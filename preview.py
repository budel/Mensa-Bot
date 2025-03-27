import os

import requests
from dotenv import load_dotenv

from menu import Menu


def preview_menus(menus_dict):
    load_dotenv()
    cookie = os.getenv("COOKIE")
    url = os.getenv("GENAI_URL")
    headers = {
        "Cookie": f"AppServiceAuthSession={cookie}",
    }

    for menu_dict in menus_dict:
        menus = Menu.from_dict(menu_dict)
        for item in menus.items:
            meal = item.name
            print(meal)

            if f"{meal}.png" in os.listdir("meals"):
                continue

            payload = {
                "messages": [
                    {
                        "content": meal,
                        "role": "user",
                    }
                ],
                "context": {
                    "overrides": {
                        "model": "dalle3",
                        "imageSize": "1792x1024",
                        "style": "vivid",
                        "quality": "hd",
                    }
                },
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                res = response.json()
                image_url = res["choices"][0]["url"]
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(f"meals/{meal}.png", "wb") as file:
                        file.write(response.content)
                    print("Image downloaded successfully.")
                else:
                    print(
                        "Failed to download image. Status code:", response.status_code
                    )
            else:
                print("Error:", response.status_code, response.text)
