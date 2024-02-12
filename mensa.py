import datetime
import requests
import json


def getMensaMenu(url, today):
    day = today.strftime("%a")
    refresh()
    url = f"https://speiseplan.mcloud.digital/meals?day={day}"
    response = requests.get(url)
    menu = json.loads(response.text)[0]
    assert menu["week"] == "current"

    meals = []
    for meal in menu["meals"]:
        if meal["location"] == "Mensa":
            meals.append(f'{meal["name"]}  \n{meal["price"]}')

    return "\n- " + "\n- ".join(meals)

def refresh():
    url = f"https://speiseplan.mcloud.digital/refresh"
    return requests.get(url)
    