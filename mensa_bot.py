import datetime
import json
import os
import sys

from burger import getBurgerMenu
import pymsteams
from dotenv import load_dotenv

from mensa import getMensaMenu
from menu import Menu
from uksh import getMFCMenu, getUKSHMenu


def main():
    load_dotenv()
    message = pymsteams.connectorcard(os.getenv("WEBHOOK"))
    message.text("Heute zum Mittagessen ... ")

    # create sections in message
    menus = create_message(message)

    # create a link to the repo
    code_section = pymsteams.cardsection()
    code_section.text(
        "<div style='text-align: right'><sup><a href='https://github.com/budel/Mensa-Bot'>Code</a></sup></div>"
    )
    message.addSection(code_section)

    message.printme()
    menus_file = "menus.json"
    menu_list = [menu.to_dict() for menu in menus]
    if len(sys.argv) > 1:
        check_for_updates(menu_list, menus_file)
    else:
        message.send()
    with open(menus_file, "w", encoding="utf-8") as f:
        json.dump(menu_list, f, indent=2, ensure_ascii=False)


def create_message(message):
    today = datetime.date.today()
    menus = []
    for menu_fn in [getMFCMenu, getUKSHMenu, getMensaMenu, getBurgerMenu]:
        section = pymsteams.cardsection()
        section.enableMarkdown()
        menu = menu_fn(today)
        menus.append(menu)
        if not menu.is_empty():
            section.text(str(menu))
        message.addSection(section)
    return menus


def check_for_updates(menu_list, menus_file="menus.json", send_on_diff=True):
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
    what = f"## [{prev.title}]({prev.url})"
    for item in prev.items:
        if cur.has_item(item):
            what += "\n- " + str(item) + "\n"
            cur.remove_item(item)
        else:
            what += "\n- <s>" + str(item) + "</s>  \n"

    # generate the new output
    idx = 0
    for item in cur.items:
        new_line = "<b>" + str(item) + "</b>\n"
        idx = what.find("</s>  \n", idx)
        offset = len("</s>  \n")
        if idx != -1:
            what = what[: idx + offset] + new_line + what[idx + offset :]
            idx += offset + len(new_line)
        else:
            what += new_line

    return what


def send_correction(text):
    message = pymsteams.connectorcard(os.getenv("WEBHOOK"))
    message.text(f"Korrektur:\n{text}")
    message.send()


if __name__ == "__main__":
    main()
