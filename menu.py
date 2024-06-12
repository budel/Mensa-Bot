class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        return f"{self.name}  \n{self.price}"

    def is_same(self, other):
        return self.name == other.name and self.price == other.price

    def to_dict(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], price=data["price"])


class Menu:
    def __init__(self, title="", url=""):
        self.title = title
        self.url = url
        self.items = []

    def __str__(self):
        header = f"## [{self.title}]({self.url})"
        return f"{header}\n- " + "\n- ".join([str(i) for i in self.items])

    def add_item(self, name, price):
        new_item = MenuItem(name, price)
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
