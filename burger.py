from menu import Menu, MenuItem

BURGER_URL = "https://www.street-gourmet.de"


class BurgerMenu(Menu):
    def __init__(self, title="", url=""):
        super().__init__(title, url)
        self.items = [
            MenuItem("Special Menü", "14,00 €"),
            MenuItem("Special Menü mit Süßkartoffelpommes", "15,00 €"),
            MenuItem("Cheeseburger", "8,50 €"),
            MenuItem("Double Cheese & Bacon", "8,90 €"),
            MenuItem("Französischer Ziegenkäse Burger", "8,90 €"),
            MenuItem("Feuriger Salsa Burger", "8,90 €"),
            MenuItem("Original Smoked BBQ-Burger", "9,50 €"),
            MenuItem("Falafel Burger", "8,50 €"),
            MenuItem("Kiwi Halloumi Burger", "8,50 €"),
            MenuItem("Jackfruit Burger", "8,90 €"),
            MenuItem("Planty of Chicken Burger", "8,90 €"),
            MenuItem("Rustic Fries", "4,50 €"),
            MenuItem("Süßkartoffelpommes", "5,50 €"),
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
            <div>14,00 €
        </li>
        <br>
        <li style="display:flex; justify-content:space-between;">
            mit Süßkartoffelpommes
            <div>15,00 €
        </li>
    </ul>
</div>
<div style="width:400px; padding:10px;">
<ul style="list-style-type: none; padding: 0;">
    <li style="display:flex; justify-content:space-between;">
        Cheeseburger
        <div>8,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Double Cheese & Bacon
        <div>8,90 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Französischer Ziegenkäse Burger</div>
        <small>mit Feigen Senf-Sauce</small></div>
        <div>8,90 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Feuriger Salsa Burger</div>
        <small>mit Jalapenos</small></div>
        <div>8,90 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        <div><div>Original Smoked BBQ-Burger</div>
        <small>mit Bacon</small></div>
        <div>9,50 €
    </li>
    <br>
    <strong>Veggie & Vegan</strong>
    <li style="display:flex; justify-content:space-between;">
        Falafel Burger
        <div>8,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Kiwi Halloumi Burger
        <div>8,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Jackfruit Burger
        <div>8,90 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Planty of Chicken Burger
        <div>8,90 €
    </li>
    <br>
    <strong>Beilagen mit Dip</strong>
    <li style="display:flex; justify-content:space-between;">
        Rustic Fries
        <div>4,50 €
    </li>
    <li style="display:flex; justify-content:space-between;">
        Süßkartoffelpommes
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
    return today.strftime("%a") == "Tue"
