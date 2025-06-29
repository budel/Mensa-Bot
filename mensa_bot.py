import datetime
import json
import logging
import pathlib

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="mensa_bot.log", encoding="utf-8", filemode="w+", level=logging.DEBUG
)
import os
import sys

from dotenv import load_dotenv

from burger import getBurgerMenu
from mensa import getMensaMenu
from menu import Menu
from message import Message
from uksh import getMFCMenu, getUKSHMenu


def main():
    logger.debug(f"main")
    load_dotenv()
    message = Message(os.getenv("WEBHOOK"))

    # create sections in message
    menus = create_message(message)

    # create a link to the repo
    message.addSection(
        "<div style='text-align: right'>"
        "<sup><a href='https://github.com/budel/Mensa-Bot'>Code</a></sup> "
        "<sup><a href='https://budel.github.io/Mensa-Bot'>Website</a></sup>"
        "</div>"
    )

    message.printme()
    menus_file = pathlib.Path(__file__).parent.resolve() / "public" / "menus.json"
    menu_list = [menu.to_dict() for menu in menus]
    if len(sys.argv) > 1:
        check_for_updates(menu_list, menus_file)
    else:
        if message.isValid():
            message.send()
    with open(menus_file, "w", encoding="utf-8") as f:
        json.dump(menu_list, f, indent=2, ensure_ascii=False)


def create_message(message):
    logger.debug(f"create_message")
    today = datetime.date.today()
    menus = []
    for menu_fn in [getMFCMenu, getMensaMenu, getUKSHMenu, getBurgerMenu]:
        menu = menu_fn(today)
        menus.append(menu)
        if not menu.is_empty():
            message.addSection(str(menu))
    return menus


def check_for_updates(menu_list, menus_file="menus.json", send_on_diff=True):
    logger.debug(f"check_for_updates")
    if os.path.exists(menus_file):
        with open(menus_file, "r") as f:
            prev_menus = json.load(f)
            for prev, cur in zip(prev_menus, menu_list):
                prev = Menu.from_dict(prev)
                cur = Menu.from_dict(cur)
                if not prev.is_same(cur):
                    if send_on_diff:
                        send_correction(what_is_different(cur, prev))
                    else:
                        return what_is_different(cur, prev)


def what_is_different(cur, prev):
    logger.debug(f"what_is_different")
    what = f"<h2><a href={prev.url}>{prev.title}</a></h2>"
    what += "\n<ul>"
    for item in prev.items:
        if cur.has_item(item):
            what += "\n<li> " + str(item) + "\n"
            cur.remove_item(item)
        else:
            what += "\n<li> <s>" + str(item) + "</s>  \n"

    # generate the new output
    idx = 0
    for item in cur.items:
        new_line = "<b>" + str(item) + "</b>\n"
        idx = what.find("</s>  \n", idx)
        offset = len("</s>  \n")
        if idx != -1:
            what = what[: idx + offset] + "<br>" + new_line + what[idx + offset :]
            idx += offset + len("<br>" + new_line)
        else:
            what += "<li>" + new_line

    what += "\n</ul>"
    return what


def send_correction(text):
    logger.debug(f"send_correction")
    message = Message(os.getenv("WEBHOOK"))
    message.addSection(f"Korrektur:<br>{text}")
    message.send()


if __name__ == "__main__":
    main()
