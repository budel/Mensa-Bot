import fitz  # PyMuPDF
import requests
import re
import pytesseract
from PIL import Image
from rapidfuzz import process, fuzz
import numpy as np

MFC_X_INIT = 735
MFC_WIDTH = 870
MFC_Y_INIT = 610
MFC_HEIGHT = 315
UKSH_X_INIT = 735
UKSH_WIDTH = 650
UKSH_Y_INIT = 590
UKSH_HEIGHT = 252
PRICE_HEIGHT = 60


def getMFCMenu(url, today):
    text, ocr, prices = parse_pdf(
        url,
        today.weekday(),
        MFC_X_INIT,
        MFC_WIDTH,
        MFC_Y_INIT,
        MFC_HEIGHT,
        3,
        price_on_lhs=False,
    )
    return compute_menu(text, ocr, prices)


def getUKSHMenu(url, today):
    text, ocr, prices = parse_pdf(
        url,
        today.weekday(),
        UKSH_X_INIT,
        UKSH_WIDTH,
        UKSH_Y_INIT,
        UKSH_HEIGHT,
        4,
        price_on_lhs=True,
    )
    return compute_menu(text, ocr, prices)


def parse_pdf(
    url, weekday, x_init, width, y_init, height, cols, price_on_lhs, filename="menu.pdf"
):
    # download_pdf(url, filename)
    texts, prices = extract_text_with_ocr(
        filename, weekday, x_init, width, y_init, height, cols, price_on_lhs
    )
    return extract_text(filename), texts, prices


def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as pdf_file:
        pdf_file.write(response.content)


def extract_text_with_ocr(
    filename, weekday, x_init, width, y_init, height, cols, price_on_lhs
):
    texts = []
    prices = []
    with fitz.open(filename) as pdf:
        assert pdf.page_count == 1
        page = pdf[0]
        for y in range(
            y_init + height * weekday,
            y_init + height * (weekday + 1),
            height,
        ):
            for x in range(x_init, x_init + width * cols, width):
                text, price = extract_text_area(
                    page, x, y, x + width, y + height, price_on_lhs
                )
                texts += [text]
                prices += [price]
    return texts, prices


def extract_text_area(page, x1, y1, x2, y2, price_on_lhs):
    # Convert to image and crop
    cell = preprocessImage(page, x1, y1, x2, y2)

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
        price_image, lang="deu", config="--oem 0 -c tessedit_char_whitelist=0123456789,/€"
    )
    # Remove all spaces and add space before and after "/"
    price = price.replace(" ", "").replace("/", " / ")

    return text, price


def preprocessImage(page, x1, y1, x2, y2, dpi=300):
    pix = page.get_pixmap(dpi=dpi)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    cropped_image = image.crop((x1, y1, x2, y2))
    # Convert the cropped image to grayscale
    gray_image = cropped_image.convert("L")
    return gray_image


def extract_text(filename):
    text = ""
    with fitz.open(filename) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text(sort=True)
    return text


def compute_menu(text, ocr, prices):
    filtered_text = filter_text(text)
    filtered_ocr = [filter_text(t) for t in ocr]
    filtered_ocr = [t for t in filtered_ocr if t]  # remove empty results
    prices = [p for p in prices if p]  # remove empty results

    menu_list = find_matches(filtered_ocr, filtered_text, prices)
    # subsets = getSubsets(filtered_text)
    # menu_list = getDailyMenu(subsets[weekday])

    return "\n- " + "\n- ".join(menu_list)


def filter_text(text):
    lines = text.splitlines()
    exclude = r"\d+|Wochentag|Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Speiseplan MFC Cafeteria|Speiseplan Bistro|/|Änderungen vorbehalten|MFC Cafeteria|Campus Lübeck|Zusatzgericht|Vegetarisch"
    filtered_text = [
        line
        for line in lines
        if line != "" and line != "-" and not re.search(exclude, line)
    ]
    return filtered_text


def find_matches(ocrs, texts, prices):
    menus = []
    for menu, price in zip(ocrs, prices):
        lines = []
        scores = []
        for line in menu:
            best_match = process.extractOne(
                line, texts, scorer=fuzz.ratio, processor=lambda s: s.lower()
            )
            lines.append(best_match[0])
            scores.append(best_match[1])
        while len(lines) > 3:  # maximal three lines per menu
            idx = np.argmin(scores)
            del lines[idx]
            del scores[idx]
        menus.append(" ".join(lines) + " " + price)
    return menus


def getSubsets(text, cols=3, lines=3):
    # Assumption: Every day has 3 meals with 3 lines each
    return [text[i : i + cols * lines] for i in range(0, len(text), cols * lines)]


def getIrregularSubsets(text, colsPerDay=[3, 4, 4, 4, 3], lines=3):
    temp = []
    i = 0
    for cols in colsPerDay:
        temp += [text[i : i + cols * lines]]
        i += cols * lines
    return temp


def getDailyMenu(text_list, cols=3, lines=3):
    menu_list = []
    for i in range(cols):
        if len(text_list) == cols * lines:
            # Every day has 3 meals with 3 lines each
            menu = [text for text in text_list[i : lines * cols : cols]]
        else:
            # No Zusatzgericht on Fridays
            return getDailyMenu(text_list, cols=2)
        menu_list.append(" ".join(menu))
    return menu_list
