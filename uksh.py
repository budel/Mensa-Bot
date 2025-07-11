import pathlib
from logging import getLogger

logger = getLogger(__name__)
import os
import re
import shutil

import fitz  # PyMuPDF
import numpy as np
import pytesseract
import requests
from PIL import Image

from menu import Menu

MFC_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/MFC+Cafeteria+im+UKSH_Verwaltungszentrum.html"
UKSH_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/UKSH_Bistro+L%C3%BCbeck-p-346.html"


def getMFCMenu(today):
    global logger
    logger = getLogger(__name__ + "_mfc")
    logger.debug("getMFCMenu called")
    return createMenu("MFC Cafeteria", MFC_URL, today, price_on_lhs=False)


def getUKSHMenu(today):
    global logger
    logger = getLogger(__name__ + "_uksh")
    logger.debug("getUKSHMenu called")
    return createMenu("UKSH Bistro", UKSH_URL, today, price_on_lhs=True)


def createMenu(title, url, today, price_on_lhs):
    try:
        url = find_pdf(url, today)
        menu = Menu(title, url)
        filename = "menu.pdf"
        prepare_pdf(url, filename)
        return parse_pdf(today, menu, price_on_lhs, filename=filename)
    except Exception as e:
        logger.debug(f"Error: {e}")
        return Menu(title, url)


def find_pdf(url, today):
    res = requests.post(url)
    if res.status_code != 200:
        return None
    kw = today.isocalendar()[1]
    pdf_link = [
        "https://www.uksh.de" + pdf_link[6:-1]
        for pdf_link in re.findall('href="[^"]+.pdf"', res.text)
        if f"KW+{kw:0>2}" in pdf_link
    ]
    if pdf_link == []:
        raise FileNotFoundError(f"Could not find this week's pdf at {url}")
    logger.info(f"pdf_link for {url}: {pdf_link[0]}")
    return pdf_link[0]


def prepare_pdf(url, filename):
    logger.debug(f"get_pdf")
    download_pdf(url, filename)
    shutil.copy(filename, "tmp.pdf")
    auto_crop_pdf("tmp.pdf", filename)
    os.remove("tmp.pdf")


def download_pdf(url, filename):
    logger.debug(f"download_pdf")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download {url}")
    with open(filename, "wb") as pdf_file:
        pdf_file.write(response.content)


def auto_crop_pdf(input_pdf, output_pdf):
    logger.debug(f"auto_crop_pdf")
    doc = fitz.open(input_pdf)
    for page in doc:
        blocks = page.get_text("dict")["blocks"]

        # Calculate minimal rect containing all text
        new_rect = fitz.Rect(10000, 10000, 0, 0)
        for block in blocks:
            r = fitz.Rect(block["bbox"])
            new_rect.include_rect(r)

        # Update page cropbox
        page.set_cropbox(new_rect)
    doc.save(output_pdf)
    doc.close()


def parse_pdf(today, menu, price_on_lhs, filename="menu.pdf", dpi=300, veggie_index=1):
    logger.debug(f"parse_pdf")
    weekday = today.weekday()
    with fitz.open(filename) as pdf:
        assert pdf.page_count > 0
        page = pdf[0]
        pil_image = preprocessImage(page, dpi=dpi)
        rows, ys = extract_weekday_rows(pil_image)
        y = ys[weekday]
        cols, xs = extract_menu_cols(rows[weekday])
        for i, (col, x) in enumerate(zip(cols, xs)):
            text, price = extract_text(pil_image, page, x, y, price_on_lhs, dpi=dpi)
            if not text:
                continue
            menu.add_item(" ".join(text), price, today, vegetarian=i == veggie_index)
    return menu


def preprocessImage(page, dpi=300):
    logger.debug(f"preprocessImage {page}")
    pix = page.get_pixmap(dpi=dpi)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Convert the cropped image to grayscale
    gray_image = image.convert("L")
    return gray_image


def extract_weekday_rows(pil_image):
    logger.debug(f"extract_weekday_rows {pil_image}")
    row_boundaries = detect_boundaries(np.asarray(pil_image), 1)
    biggest_rows = get_biggest_boundaries(row_boundaries)
    return [
        pil_image.crop((0, upper, pil_image.width, lower))
        for (upper, lower) in sorted(biggest_rows)
    ], sorted(biggest_rows)


def extract_menu_cols(row):
    logger.debug(f"extract_menu_cols {row}")
    col_boundaries = detect_boundaries(np.asarray(row), 0)
    biggest_cols = get_biggest_boundaries(col_boundaries)
    return [
        row.crop((left, 0, right, row.height)) for (left, right) in sorted(biggest_cols)
    ], sorted(biggest_cols)


def get_biggest_boundaries(boundaries):
    logger.debug(f"get_biggest_boundaries {boundaries}")
    # we assume that our rows/column are bigger than the first row/column
    diffs = np.diff(boundaries)
    start = [b for d, b in sorted(zip(diffs, boundaries), reverse=True) if d > diffs[0]]
    end = [
        b for d, b in sorted(zip(diffs, boundaries[1:]), reverse=True) if d > diffs[0]
    ]
    return list(zip(start, end))


def detect_boundaries(image, axis):
    logger.debug(f"detect_boundaries {image}, {axis}")
    modes = np.apply_along_axis(mode, axis, image)
    previous_pixel = modes[0]
    boundaries = []
    for i, current_pixel in enumerate(modes):
        if previous_pixel != current_pixel:
            boundaries.append(i)
            previous_pixel = current_pixel

    return [0] + boundaries + [len(modes)]


def mode(a):
    u, c = np.unique(a, return_counts=True)
    return u[c.argmax()]


def extract_text(pil_image, page, x, y, price_on_lhs, dpi=300):
    logger.debug(f"extract_text")
    f = 72 / dpi
    rect = fitz.Rect(x[0] * f, y[0] * f, x[1] * f, y[1] * f)
    text = page.get_text(sort=True, clip=rect)
    price = get_price(pil_image, x, y, price_on_lhs, dpi=dpi)
    return filter_text(text), price


def get_price(pil_image, x, y, price_on_lhs, dpi=300):
    logger.debug(f"get_price")
    xNew = [x[0], (x[0] + x[1]) / 2.0] if price_on_lhs else [(x[0] + x[1]) / 2.0, x[1]]
    cell = pil_image.crop((xNew[0], y[1] - 0.2 * dpi, xNew[1], y[1]))
    text = pytesseract.image_to_string(
        cell,
        lang="Netto",
        config=f"--tessdata-dir {pathlib.Path(__file__).parent.resolve()} --psm 7 -c tessedit_char_whitelist=0123456789,/€",
    )
    text = text.replace(" ", "").replace("/", " / ")
    if re.match(r"€\d+,\d\d \/ €\d+,\d\d", text):
        return text
    else:
        # Fallback to Legacy engine only
        text = pytesseract.image_to_string(
            cell,
            lang="deu",
            config=f"--tessdata-dir {pathlib.Path(__file__).parent.resolve()} --oem 0 --psm 7 -c tessedit_char_whitelist=0123456789,/€",
        )
        text = text.replace(" ", "").replace("/", " / ")
        return text


def filter_text(text):
    logger.debug(f"filter_text")
    lines = text.splitlines()
    exclude = r"\d+|Wochentag|Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|Speiseplan MFC Cafeteria|Speiseplan Bistro|/|Änderungen vorbehalten|MFC Cafeteria|Campus Lübeck|Zusatzgericht|Vegetarisch|Öffnungszeiten"
    filtered_text = [
        line
        for line in lines
        if line != "" and line != "-" and not re.search(exclude, line)
    ]
    return filtered_text
