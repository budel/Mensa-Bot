from datetime import datetime
from typing import Dict, Any


class MenuItem:

    def __init__(
        self,
        name: str,
        price: str,
        date: datetime,
        vegetarian: bool,
        vegan: bool,
    ):
        self.name = name
        self.price = price
        self.date = date
        self.vegetarian = vegetarian
        self.vegan = vegan

    def __lt__(self, other: "MenuItem") -> bool:
        return self.name < other.name

    def __str__(self) -> str:
        v_icon = "&#127793;" if self.is_veggie() else ""
        return f"{v_icon} {self.name}<br>{self.price}"

    def is_same(self, other: "MenuItem") -> bool:
        return self.name == other.name and self.price == other.price

    def is_veggie(self) -> bool:
        return self.vegetarian or self.vegan

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "price": self.price,
            "vegetarian": self.vegetarian,
            "vegan": self.vegan,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MenuItem":
        return cls(
            name=data["name"],
            price=data["price"],
            vegetarian=data["vegetarian"],
            vegan=data["vegan"],
            date=datetime.fromisoformat(data["date"]),
        )


class Menu:
    def __init__(self, title: str = "", url: str = ""):
        self.title = title
        self.url = url
        self.items = []

    def __str__(self) -> str:
        header = f"<h2><a href={self.url}>{self.title}</a></h2>"
        list_items = "\n".join(f"<li>{str(i)}" for i in self.items)
        return f"{header}\n<ul>\n{list_items}\n</ul>"

    def add_item(
        self,
        name: str,
        price: str,
        date: datetime,
        vegetarian: bool = False,
        vegan: bool = False,
    ) -> None:
        new_item = MenuItem(name, price, date, vegetarian, vegan)
        self.items.append(new_item)

    def is_empty(self) -> bool:
        return self.items == []

    def is_same(self, other: "Menu") -> bool:
        return (
            self.title == other.title
            and self.url == other.url
            and len(self.items) == len(other.items)
            and all(
                s.is_same(o) for s, o in zip(sorted(self.items), sorted(other.items))
            )
        )

    def has_item(self, item: MenuItem) -> bool:
        for i in self.items:
            if i.is_same(item):
                return True
        return False

    def remove_item(self, item: MenuItem) -> None:
        for i in self.items:
            if i.is_same(item):
                self.items.remove(i)
                break

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Menu":
        menu = cls(title=data["title"], url=data["url"])
        # Add each item from the dictionary to the menu
        for item in data["items"]:
            menu.add_item(
                item["name"],
                item["price"],
                item["date"],
                item["vegetarian"],
                item["vegan"],
            )
        return menu
