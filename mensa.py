import requests
import json
from menu import Menu


def getMensaMenu(url, today):
    day = today.strftime("%a")
    refresh()
    url = f"https://speiseplan.mcloud.digital/meals?day={day}"
    response = requests.get(url)
    menu_dict = json.loads(response.text)[0]

    menu = Menu()
    for meal in menu_dict["meals"]:
        if meal["location"] == "Mensa":
            menu.add_item(meal["name"], meal["price"])

    return menu


def refresh():
    url = f"https://speiseplan.mcloud.digital/refresh"
    return requests.get(url)
