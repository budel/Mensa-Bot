import datetime
import requests
import json


def getMensaMenu(url):
    day = datetime.date.today().strftime("%a")
    url = f"https://speiseplan.mcloud.digital/meals?day={day}"
    response = requests.get(url)
    menu = json.loads(response.text)[0]
    assert menu["week"] == "current"

    meals = []
    for meal in menu["meals"]:
        if meal["location"] == "Mensa":
            meals.append(meal["name"])

    return "\n- " + "\n- ".join(meals)