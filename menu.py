class MenuItem:
    def __init__(self, name, price, vegetarian, vegan):
        self.name = name
        self.price = price
        self.vegetarian = vegetarian
        self.vegan = vegan

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f"{self.name}<br>{self.price}"

    def is_same(self, other):
        return self.name == other.name and self.price == other.price

    def is_veggie(self):
        return self.vegetarian or self.vegan

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "vegetarian": self.vegetarian,
            "vegan": self.vegan,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            price=data["price"],
            vegetarian=data["vegetarian"],
            vegan=data["vegan"],
        )


class Menu:
    def __init__(self, title="", url=""):
        self.title = title
        self.url = url
        self.items = []

    def __str__(self):
        header = f"<h2><a href={self.url}>{self.title}</a></h2>"
        list_items = "\n".join(
            (
                f"<li>&#127793; {str(i)}"
                if i.is_veggie()
                else f"<li>{str(i)}"
            )
            for i in self.items
        )
        return f"{header}\n<ul>\n{list_items}\n</ul>"

    def add_item(self, name, price, vegetarian=False, vegan=False):
        new_item = MenuItem(name, price, vegetarian, vegan)
        self.items.append(new_item)

    def is_empty(self):
        return self.items == []

    def is_same(self, other):
        return (
            self.title == other.title
            and self.url == other.url
            and len(self.items) == len(other.items)
            and all(
                s.is_same(o) for s, o in zip(sorted(self.items), sorted(other.items))
            )
        )

    def has_item(self, item):
        for i in self.items:
            if i.is_same(item):
                return True
        return False

    def remove_item(self, item):
        for i in self.items:
            if i.is_same(item):
                self.items.remove(i)
                break

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data):
        menu = cls(title=data["title"], url=data["url"])
        # Add each item from the dictionary to the menu
        for item in data["items"]:
            menu.add_item(item["name"], item["price"])
        return menu
