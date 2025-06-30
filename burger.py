from menu import Menu, MenuItem

BURGER_URL = "https://www.street-gourmet.de"


class BurgerMenu(Menu):
    def __init__(self, title="", url=""):
        super().__init__(title, url)
        self.items = [
            MenuItem("Cheeseburger", "9,00 €", vegetarian=False, vegan=False),
            MenuItem("Double Cheese & Bacon", "9,50 €", vegetarian=False, vegan=False),
            MenuItem(
                "Französischer Ziegenkäse Burger mit Feigen Senf-Sauce",
                "9,50 €",
                vegetarian=False,
                vegan=False,
            ),
            MenuItem(
                "Feuriger Salsa Burger mit Jalapenos",
                "9,50 €",
                vegetarian=False,
                vegan=False,
            ),
            MenuItem(
                "Original Smoked BBQ-Burger mit Bacon",
                "10,00 €",
                vegetarian=False,
                vegan=False,
            ),
            MenuItem("Falafel Burger", "9,00 €", vegetarian=True, vegan=False),
            MenuItem("Kiwi Halloumi Burger", "9,00 €", vegetarian=True, vegan=False),
            MenuItem("Jackfruit Burger", "9,50 €", vegetarian=True, vegan=False),
            MenuItem(
                "Planty of Chicken Burger", "10,00 €", vegetarian=True, vegan=False
            ),
            MenuItem("Rustic Fries", "4,50 €", vegetarian=True, vegan=False),
            MenuItem("Süßkartoffelpommes", "5,50 €", vegetarian=True, vegan=False),
        ]

    def __str__(self):
        return f"""
<h2><a href={self.url}>{self.title}</a></h2>
<div style="width:400px; height:135px; border:2px solid black; padding:10px;">
    <strong>Special Menü</strong>
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li>✓ Alle Burger
        <li>✓ Rustic Fries mit Dip
        <li style="display:flex; justify-content:space-between;">
            ✓ Drink
            <div>15,00 €
        </li>
        <br>
        <li style="display:flex; justify-content:space-between;">
            mit Süßkartoffelpommes
            <div>16,00 €
        </li>
    </ul>
</div>
<div style="width:400px; padding:10px;">
<ul style="list-style-type: none; padding: 0;">
    <li style="display:flex; justify-content:space-between;">
        Cheeseburger
        <div>9,00 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Double Cheese & Bacon
        <div>9,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Französischer Ziegenkäse Burger</div>
        <small>mit Feigen Senf-Sauce</small></div>
        <div>9,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Feuriger Salsa Burger</div>
        <small>mit Jalapenos</small></div>
        <div>9,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Original Smoked BBQ-Burger</div>
        <small>mit Bacon</small></div>
        <div>10,00 €
    </li>
    <br>
    <strong>Veggie & Vegan</strong>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Falafel Burger
        <div>9,00 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Kiwi Halloumi Burger
        <div>9,00 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Jackfruit Burger
        <div>9,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Planty of Chicken Burger
        <div>10,00 €
    </li>
    <br>
    <strong>Beilagen mit Dip</strong>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Rustic Fries
        <div>4,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        &#127793;Süßkartoffelpommes
        <div>5,50 €
    </li>
</ul>
</div>
  """


def getBurgerMenu(today):
    if isBurgerDay(today):
        return BurgerMenu("Foodtruck", BURGER_URL)
    else:
        return Menu("Foodtruck", BURGER_URL)


def isBurgerDay(today):
    return today.weekday() == 1
