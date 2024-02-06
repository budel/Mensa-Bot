import datetime
import os
import re

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
    message.send()


def create_message(mfc_link, uksh_link, mensa_link, message):
    today = weekday = datetime.date.today()
    for m_link, m_name in zip(
        [mfc_link, uksh_link, mensa_link],
        ["MFC Cafeteria", "UKSH Bistro", "Studenten Mensa"],
    ):
        section = pymsteams.cardsection()
        section.linkButton(m_name, m_link)
        message.addSection(section)

        section = pymsteams.cardsection()
        section.enableMarkdown()
        text = ""
        if "MFC" in m_name:
            text += getMFCMenu(m_link, today)
        if "UKSH" in m_name:
            text += getUKSHMenu(m_link, today)
        elif "Mensa" in m_name:
            text += getMensaMenu(m_link, today)
        section.text(text)
        message.addSection(section)


if __name__ == "__main__":
    send_message(find_pdf(MFC_URL), find_pdf(UKSH_URL), MENSA_URL)
