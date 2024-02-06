import datetime
from mensa import getMensaMenu
from mensa_bot import MENSA_URL, MFC_URL, UKSH_URL, find_pdf

from uksh import (
    MFC_HEIGHT,
    MFC_WIDTH,
    MFC_X_INIT,
    MFC_Y_INIT,
    UKSH_HEIGHT,
    UKSH_WIDTH,
    UKSH_X_INIT,
    UKSH_Y_INIT,
    getMFCMenu,
    getUKSHMenu,
    parse_pdf,
)
import pytest


@pytest.mark.skip()
def testMFC():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text = getMFCMenu(find_pdf(MFC_URL), day)
        print(text)


@pytest.mark.skip()
def testMFCParser():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text, ocr, prices = parse_pdf(
            find_pdf(MFC_URL),
            day.weekday(),
            MFC_X_INIT,
            MFC_WIDTH,
            MFC_Y_INIT,
            MFC_HEIGHT,
            3,
            price_on_lhs=False,
        )
        print(" ".join(ocr))
        print(" ".join(prices))


@pytest.mark.skip()
def testUKSH():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text = getUKSHMenu(find_pdf(UKSH_URL), day)
        print(text)


@pytest.mark.skip()
def testUKSHParser():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text, ocr, prices = parse_pdf(
            find_pdf(UKSH_URL),
            day.weekday(),
            UKSH_X_INIT,
            UKSH_WIDTH,
            UKSH_Y_INIT,
            UKSH_HEIGHT,
            4,
            price_on_lhs=True,
        )
        print(" ".join(ocr))
        print(" ".join(prices))


@pytest.mark.skip()
def testMensa():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    for i in range(5):
        day = start_of_week + datetime.timedelta(days=i)
        text = getMensaMenu(MENSA_URL, day)
        print(text)
