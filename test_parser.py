import datetime
from mensa import getMensaMenu
from mensa_bot import find_pdf

from uksh import (
    MFC_HEIGHT,
    MFC_WIDTH,
    MFC_X_INIT,
    MFC_Y_INIT,
    getMFCMenu,
    getUKSHMenu,
    parse_pdf,
)
import pytest


MFC_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/MFC+Cafeteria+im+UKSH_Verwaltungszentrum.html"
UKSH_URL = "https://www.uksh.de/ssn/Unser+Speisenangebot/Campus+L%C3%BCbeck/UKSH_Bistro+L%C3%BCbeck-p-346.html"
MENSA_URL = "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan"

@pytest.mark.skip()
def testMFC():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text = getMFCMenu(find_pdf(MFC_URL), day)
        print(text)


def testMFCParser():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text, ocr = parse_pdf(
            find_pdf(MFC_URL),
            day.weekday(),
            MFC_X_INIT,
            MFC_WIDTH,
            MFC_Y_INIT,
            MFC_HEIGHT,
            3,
        )
        print(" ".join(ocr))

