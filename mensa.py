import locale
import logging

logger = logging.getLogger(__name__)
import requests
import json
from menu import Menu

MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"
LOCATION_CAFETERIA="HL_CA"
LOCATION_MENSA="HL_ME"


def getMensaMenu(today):
    menu = Menu("Studenten Mensa", MENSA_URL)

    logger.debug(f"getMensaMenu")
    day = today.strftime("%Y-%m-%d")
    url = f"https://speiseplan.mcloud.digital/v2/meals?location={LOCATION_MENSA}&date={day}"
    response = requests.get(url)
    if response.status_code == 200:
        menu_dict = json.loads(response.text)
    else:
        logger.debug(f"Failed to download {url}")
        menu.add_item(f"Konnte {url} nicht erreichen.", "", today)
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
