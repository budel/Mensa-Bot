import logging
logger = logging.getLogger(__name__)
import requests
import json
from menu import Menu

MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"

def getMensaMenu(today):
    logger.debug(f"getMensaMenu")
    day = today.strftime("%a")
    refresh()
    url = f"https://speiseplan.mcloud.digital/meals?day={day}"
    response = requests.get(url)
    menu_dict = json.loads(response.text)[0]

    menu = Menu("Studenten Mensa", MENSA_URL)
    for meal in menu_dict["meals"]:
        if meal["location"] == "Mensa":
            menu.add_item(meal["name"], meal["price"])

    return menu


def refresh():
    logger.debug(f"refresh")
    url = f"https://speiseplan.mcloud.digital/refresh"
    return requests.get(url)
