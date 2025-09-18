import locale
import logging

logger = logging.getLogger(__name__)
import requests
import json
from fetch_mensa import fetch_mensa
from menu import Menu

MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"
BB_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=17#mensaplan"


def getBitsBytesMenu(today):
    return getMenu(today, "Bits + Bytes", "HL_BB", BB_URL)

def getCafeteriaMenu(today):
    return getMenu(today, "Studenten Cafeteria", "HL_CA", MENSA_URL)

def getMensaMenu(today):
    return getMenu(today, "Studenten Mensa", "HL_ME", MENSA_URL)

def getMenu(today, name, location, url):
    logger.debug(f"getMensaMenu")
    menu = Menu(name, url)
    day = today.strftime("%Y-%m-%d")
    try:
        json_str = fetch_mensa()
        menu_dicts = json.loads(json_str)
        # Filter menu by location and date
        menu_dicts = [m for m in menu_dicts if m["location"]["code"] == location and m["date"] == day and m["language"]["code"] == "de"]
    except:
        logger.debug(f"Failed to download {url}")
        menu.add_item(f"Fehler beim Holen von {url}", "", today)
        return menu

    for meal in menu_dicts:
        prices = " / ".join(map(formatPrice, meal["price"].values()))
        prices = "" if prices == "0.00 € / 0.00 € / 0.00 €" else prices
        menu.add_item(
            meal["name"],
            prices,
            today,
            vegetarian=meal["vegetarian"],
            vegan=meal["vegan"],
        )

    return menu


def formatPrice(price):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return locale.format_string("%.2f €", price, grouping=True)
