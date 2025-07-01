import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="mensa_bot.log", encoding="utf-8", filemode="w+", level=logging.DEBUG
)
import os
import requests

from dotenv import load_dotenv

from menu import Menu
from message import Message

MENUS_URL = "https://budel.github.io/Mensa-Bot/menus.json"


def main():
    logger.debug(f"main")
    load_dotenv()
    message = Message(os.getenv("WEBHOOK"))

    message.addSection(
        "<h2>"
        "The menu now has its own <a href='https://budel.github.io/Mensa-Bot'>Website</a>!"
        "</h2><br>"
    )

    # create sections in message
    response = requests.get(MENUS_URL)
    data = response.json()
    parse_menu(message, data)

    # create a link to the repo
    message.addSection(
        "<div style='text-align: right'>"
        "<sup><a href='https://github.com/budel/Mensa-Bot'>Code</a></sup> "
        "</div>"
    )

    message.printme()
    if message.isValid():
        message.send()


def parse_menu(message, all_menus):
    logger.debug(f"parse_menu")
    today = datetime.date.today().isoformat()

    for daily_menus in all_menus:
        for menu_dict in daily_menus:
            menu = Menu.from_dict(menu_dict)
            isTodaysMenu = any(item.date == today for item in menu.items)
            if isTodaysMenu and not menu.is_empty():
                message.addSection(str(menu))


if __name__ == "__main__":
    main()
