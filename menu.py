class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}  \n{self.price}"


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
