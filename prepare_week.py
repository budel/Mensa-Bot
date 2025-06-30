import datetime
import json
import os
import pathlib

from burger import getBurgerMenu
from mensa import getMensaMenu
from uksh import getMFCMenu, getUKSHMenu


def main():
    menus_file = parse_week()
    print(f"Menus for the week saved to: {menus_file}")
    menus_file = parse_week(datetime.date.today() + datetime.timedelta(days=7))
    print(f"Menus for the next week saved to: {menus_file}")


def parse_week(today=datetime.date.today()):
    monday = today - datetime.timedelta(days=today.weekday())

    menus_file = (
        pathlib.Path(__file__).parent.resolve() / "public" / f"menus-{monday}.json"
    )
    if os.path.exists(menus_file):
        return menus_file

    menu_list = []
    for i in range(5):
        day = monday + datetime.timedelta(days=i)
        menus_per_day = []
        for menu_fn in [getMFCMenu, getMensaMenu, getUKSHMenu, getBurgerMenu]:
            menu = menu_fn(day)
            menus_per_day.append(menu)
        menu_list.append([menu.to_dict() for menu in menus_per_day])

    with open(menus_file, "w", encoding="utf-8") as f:
        json.dump(menu_list, f, indent=2, ensure_ascii=False)

    return menus_file


if __name__ == "__main__":
    main()
