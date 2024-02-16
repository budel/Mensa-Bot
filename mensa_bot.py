import datetime
import json
import os
import re
import sys

import pymsteams
import requests
from dotenv import load_dotenv

from mensa import getMensaMenu
from uksh import getMFCMenu, getUKSHMenu

MFC_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/MFC+Cafeteria+im+UKSH_Verwaltungszentrum.html"
UKSH_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/UKSH_Bistro+L%C3%BCbeck-p-346.html"
MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"


def find_pdf(url):
    res = requests.post(url)
    if (res.status_code != 200):
        return None
    kw = datetime.date.today().isocalendar()[1]
    pdf_link = [
        "https://www.uksh.de" + pdf_link[6:-1]
        for pdf_link in re.findall('href="[^"]+.pdf"', res.text)
        if f"KW+{kw:0>2}" in pdf_link
    ]

    return pdf_link[0]


def send_message(mfc_link, uksh_link, mensa_link):
    load_dotenv()
    message = pymsteams.connectorcard(os.getenv("WEBHOOK"))
    message.text("Heute zum Mittagessen ... ")

    # create sections in message
    create_message(mfc_link, uksh_link, mensa_link, message)

    # create the Burger section
    if datetime.date.today().strftime("%a") == "Tue":
        burger_section = pymsteams.cardsection()
        burger_section.text("... und nicht vergessen, heute ist Burger Tag!")
        message.addSection(burger_section)

    # create a link to the repo
    code_section = pymsteams.cardsection()
    code_section.text(
        "<div style='text-align: right'><sup><a href='https://github.com/budel/Mensa-Bot'>Code</a></sup></div>"
    )
    message.addSection(code_section)

    message.printme()
    payload_file = 'payload.json'
    if len(sys.argv) > 1:
        check_for_updates(message, payload_file)
    else:
        message.send()
    with open(payload_file, 'w') as f:
        json.dump(message.payload, f)



def create_message(mfc_link, uksh_link, mensa_link, message):
    today = datetime.date.today()
    for m_link, m_name in zip(
        [mfc_link, uksh_link, mensa_link],
        ["MFC Cafeteria", "UKSH Bistro", "Studenten Mensa"],
    ):
        if(m_link):
            section = pymsteams.cardsection()
            section.enableMarkdown()
            text = f"## [{m_name}]({m_link})\n"
            if "MFC" in m_name:
                text += getMFCMenu(m_link, today)
            if "UKSH" in m_name:
                text += getUKSHMenu(m_link, today)
            elif "Mensa" in m_name:
                text += getMensaMenu(m_link, today)
            section.text(text)
            message.addSection(section)
        else:
            section = pymsteams.cardsection()
            section.text(f"Kein Speiseplan für {m_name} gefunden.")
            message.addSection(section)


def check_for_updates(message, payload_file = 'payload.json'):
    if os.path.exists(payload_file):
        with open(payload_file, "r") as f:
            prev_payload = json.load(f)
            for prev, cur in zip(prev_payload["sections"], message.payload['sections']):
                if cur['text'] != prev['text']:
                    print(cur['text'])
                    send_correction(cur['text'])
 

def send_correction(text):
    message = pymsteams.connectorcard(os.getenv("WEBHOOK"))
    message.text(f"Korrektur:\n{text}")
    message.send()


if __name__ == "__main__":
    send_message(find_pdf(MFC_URL), find_pdf(UKSH_URL), MENSA_URL)
