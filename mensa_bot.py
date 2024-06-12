import datetime
import json
import os
import re
import sys

from burger import getBurgerMenu, isBurgerDay
import pymsteams
import requests
from dotenv import load_dotenv

from mensa import getMensaMenu
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
    payload_file = "payload.json"
    if len(sys.argv) > 1:
        check_for_updates(message, payload_file)
    else:
        message.send()
    with open(payload_file, "w") as f:
        json.dump(message.payload, f)


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


def check_for_updates(message, payload_file="payload.json", send_on_diff=True):
    if os.path.exists(payload_file):
        with open(payload_file, "r") as f:
            prev_payload = json.load(f)
            for prev, cur in zip(prev_payload["sections"], message.payload["sections"]):
                if is_different(cur["text"], prev["text"]):
                    print(cur["text"])
                    if send_on_diff:
                        send_correction(what_is_different(cur["text"], prev["text"]))
                    else:
                        return what_is_different(cur["text"], prev["text"])


def is_different(cur, prev):
    if cur == prev:
        return False
    if is_different_order(cur, prev):
        return False
    return True


def is_different_order(cur, prev):
    return "\n".join(sorted(cur.splitlines())) == "\n".join(sorted(prev.splitlines()))


def what_is_different(cur, prev):
    cur_lines = cur.split("\n-")
    prev_lines = prev.split("\n-")

    what = prev_lines[0]  # Link to menu
    for line in prev_lines[1:]:
        if line in cur_lines:
            what += "\n-" + line + "\n"
            cur_lines.remove(line)
        else:
            what += "\n- <s>" + line + "</s>  \n"

    # print the new lines
    idx = 0
    for line in cur_lines[1:]:
        new_line = "<b>" + line + "</b>\n"
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
