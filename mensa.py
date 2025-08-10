import locale
import logging

logger = logging.getLogger(__name__)
import requests
import json
from fetch_mensa import fetch_mensa
from menu import Menu

MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"


def getCafeteriaMenu(today):
    return getMenu(today, "Studenten Cafeteria", "HL_CA")

def getMensaMenu(today):
    return getMenu(today, "Studenten Mensa", "HL_ME")

def getMenu(today, name, location):
    logger.debug(f"getMensaMenu")
    menu = Menu(name, MENSA_URL)
    day = today.strftime("%Y-%m-%d")
    url = f"http://localhost:3030/v2/meals?location={location}&date={day}"
    try:
        json_str = fetch_mensa()
        menu_dict = json.loads(json_str)
        # Filter menu by location and date
    except:
        logger.debug(f"Failed to download {url}")
        menu.add_item(f"Fehler beim Holen von {url}", "", today)
        return menu

    for meal in menu_dict["data"]:
        prices = " / ".join(map(formatPrice, meal["price"].values()))
        prices = "" if prices == "0.0 / 0.0 / 0.0" else prices
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
