from logging import getLogger

logger = getLogger(__name__)
import os
import shutil
import fitz  # PyMuPDF
import requests
import re
import pytesseract
from PIL import Image
from rapidfuzz import process, fuzz
import numpy as np

from menu import Menu

MFC_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/MFC+Cafeteria+im+UKSH_Verwaltungszentrum.html"
UKSH_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/UKSH_Bistro+L%C3%BCbeck-p-346.html"
PRICE_HEIGHT = 60


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
    logger.info(f"pdf_link for {url}: {pdf_link[0]}")
    return pdf_link[0]


def getMFCMenu(today):
    global logger
    logger = getLogger(__name__ + "_mfc")
    logger.debug("getMFCMenu called")
    try:
        url = find_pdf(MFC_URL, today)
        text, ocr, prices = parse_pdf(url, today.weekday(), price_on_lhs=False)
        return compute_menu(text, ocr, prices, "MFC Cafeteria", url)
    except Exception as e:
        logger.debug(f"Exception in getMFCMenu: {e}")
        return Menu("MFC Cafeteria", url)


def getUKSHMenu(today):
    global logger
    logger = getLogger(__name__ + "_uksh")
    logger.debug("getUKSHMenu called")
    try:
        url = find_pdf(UKSH_URL, today)
        text, ocr, prices = parse_pdf(url, today.weekday(), price_on_lhs=True)
        return compute_menu(text, ocr, prices, "UKSH Bistro", url)
    except Exception as e:
        logger.debug(f"Exception in getUKSHMenu: {e}")
        return Menu("UKSH Bistro", url)


def parse_pdf(url, weekday, price_on_lhs, filename="menu.pdf"):
    logger.debug(f"parse_pdf")
    download_pdf(url, filename)
    shutil.copy(filename, "tmp.pdf")
    auto_crop_pdf("tmp.pdf", filename)
    os.remove("tmp.pdf")
    texts, prices = extract_text_with_ocr(filename, weekday, price_on_lhs)
    return extract_text(filename), texts, prices


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


def extract_text_with_ocr(filename, weekday, price_on_lhs):
    logger.debug(f"extract_text_with_ocr")
    texts = []
    prices = []
    with fitz.open(filename) as pdf:
        assert pdf.page_count == 1
        page = pdf[0]
        pil_image = preprocessImage(page)
        row = extract_weekday_row(pil_image)
        for cell in extract_menu_cols(row[weekday]):
            text, price = extract_text_area(row, cell, price_on_lhs)
            texts += [text]
            prices += [price]
    return texts, prices


def extract_weekday_row(pil_image):
    logger.debug(f"extract_weekday_row {pil_image}")
    row_boundaries = detect_boundaries(np.asarray(pil_image), 1)
    biggest_rows = get_biggest_boundaries(row_boundaries)
    return [
        pil_image.crop((0, upper, pil_image.width, lower))
        for (upper, lower) in sorted(biggest_rows)
    ]


def extract_menu_cols(row):
    logger.debug(f"extract_menu_cols {row}")
    col_boundaries = detect_boundaries(np.asarray(row), 0)
    biggest_cols = get_biggest_boundaries(col_boundaries)
    return [
        row.crop((left, 0, right, row.height)) for (left, right) in sorted(biggest_cols)
    ]


def preprocessImage(page, dpi=300):
    logger.debug(f"preprocessImage {page}")
    pix = page.get_pixmap(dpi=dpi)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Convert the cropped image to grayscale
    gray_image = image.convert("L")
    return gray_image


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


def extract_text_area(row, cell, price_on_lhs):
    logger.debug(f"extract_text_area {row}, {cell}, {price_on_lhs}")
    # Perform OCR on the grayscale image using Tesseract
    text = pytesseract.image_to_string(cell, lang="deu")

    # focus only on price (lower part of cell)
    if price_on_lhs:
        price_image = cell.crop(
            (0, cell.height - PRICE_HEIGHT, cell.width // 2, cell.height)
        )
    else:
        price_image = cell.crop(
            (cell.width // 2, cell.height - PRICE_HEIGHT, cell.width, cell.height)
        )
    price = pytesseract.image_to_string(
        price_image,
        lang="deu",
        config="--oem 0 -c tessedit_char_whitelist=0123456789,/€",
    )
    # Remove all spaces and add space before and after "/"
    price = price.replace(" ", "").replace("/", " / ")

    logger.info(f"extract_text_area found {text}, {price}")
    return text, price


def extract_text(filename):
    logger.debug(f"extract_text")
    text = ""
    with fitz.open(filename) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text(sort=True)
    logger.info(f"extract_text found {text}")
    return text


def compute_menu(text, ocr, prices, title, url):
    logger.debug(f"compute_menu")
    filtered_text = filter_text(text)
    filtered_ocr = [filter_text(t) for t in ocr]
    menu = Menu(title, url)
    return find_matches(filtered_ocr, filtered_text, prices, menu)


def filter_text(text):
    logger.debug(f"filter_text")
    lines = text.splitlines()
    exclude = r"\d+|Wochentag|Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag|Speiseplan MFC Cafeteria|Speiseplan Bistro|/|Änderungen vorbehalten|MFC Cafeteria|Campus Lübeck|Zusatzgericht|Vegetarisch"
    filtered_text = [
        line
        for line in lines
        if line != "" and line != "-" and not re.search(exclude, line)
    ]
    return filtered_text


def find_matches(ocrs, texts, prices, menu, veggie_index=1):
    logger.debug(f"find_matches")
    for i, (meal, price) in enumerate(zip(ocrs, prices)):
        if not meal or not price:
            continue
        lines = []
        scores = []
        for line in meal:
            best_match = process.extractOne(
                line, texts, scorer=fuzz.ratio, processor=lambda s: s.lower()
            )
            lines.append(best_match[0])
            scores.append(best_match[1])
        while len(lines) > 3:  # maximal three lines per menu
            idx = np.argmin(scores)
            del lines[idx]
            del scores[idx]
        menu.add_item(" ".join(lines), price, vegetarian=i == veggie_index)
    return menu
