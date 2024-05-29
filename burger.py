
def isBurgerDay(today):
  return today.strftime("%a") == "Tue"

def getBurgerMenu():
    return """
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
