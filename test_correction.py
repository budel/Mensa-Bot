import pytest
from mensa_bot import check_for_updates


class Message:
    def __init__(self):
        self.payload = {
            "sections": [
                {
                    "text": """## [MFC Cafeteria](https://www.uksh.de/uksh_media/Speisepl%C3%A4ne/L%C3%BCbeck+_+MFC+Cafeteria/KW+18+Speiseplan+MFC+29_04_2024+_+03_05_2024-p-776281.pdf)

- Schweinefiletmedaillions mit Pfefferrahmsauce, frischem Spargel dazu Kroketten  
€9,20 / €12,24

- Frischkäsekartoffeltaschen am bunten Salatbouquet mit Tomatenkräuterdip  
€4,15 / €5,52

- Lasagne Bolognese mit Tomatensauce dazu ein Beilagensalat  
€6,20 / €8,25
"""
                },
                {
                    "text": """## [UKSH Bistro](https://www.uksh.de/uksh_media/Speisepl%C3%A4ne/L%C3%BCbeck+_+UKSH_Bistro/KW+18+Speiseplan+Bistro+29_04_2024+_+05_05_2024-p-776270.pdf)

- Frischkäsekartoffeltaschen am bunten Salatbouquet mit Tomatenkräuterdip  
€4,15 / €5,52

- Schweinefiletmedaillions mit Pfefferrahmsauce, frischem Spargel dazu Kroketten  
€9,20 / €12,24

- Lasagne Bolognese mit Tomatensauce dazu ein Beilagensalat  
€6,20 / €8,25
"""
                },
                {
                    "text": """## [Studenten Mensa](https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan)

- Grüne- Thai- Kokos- Gemüsesuppe, Ingwer, Mie-Nudeln, Koriander, Baguettebrot  
2,50 € / 4,30 € / 5,00 €
- Quinoa [Bio]- Bowl - Spinat-Hummus, Brokkoli, Karotten, Ingwer, Casshewkerne  
3,50 € / 5,30 € / 6,00 €
- Chicken Makhani, Basmatireis, Indisches Butterhuhn, Joghurt[Bio], Tomate, Mandeln  
2,50 € / 5,40 € / 6,10 €
- Tagesgericht: Röstkartoffeln, mediterranes Gemüse, Kräuterquark  
3,80 € / 3,80 € / 3,80 €
- . und Hähnchen vom Grill  
2,00 € / 2,00 € / 2,00 €
- Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch  
"""
                },
            ]
        }


def test_check_for_updates_without_diff():
    message = Message()
    out = check_for_updates(message, "payload.json", send_on_diff=False)
    assert out == None


def test_check_for_updates_with_different_order():
    message = Message()
    message.payload["sections"][2][
        "text"
    ] = """## [Studenten Mensa](https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan)

- Chicken Makhani, Basmatireis, Indisches Butterhuhn, Joghurt[Bio], Tomate, Mandeln  
2,50 € / 5,40 € / 6,10 €
- Grüne- Thai- Kokos- Gemüsesuppe, Ingwer, Mie-Nudeln, Koriander, Baguettebrot  
2,50 € / 4,30 € / 5,00 €
- Quinoa [Bio]- Bowl - Spinat-Hummus, Brokkoli, Karotten, Ingwer, Casshewkerne  
3,50 € / 5,30 € / 6,00 €
- Tagesgericht: Röstkartoffeln, mediterranes Gemüse, Kräuterquark  
3,80 € / 3,80 € / 3,80 €
- . und Hähnchen vom Grill  
2,00 € / 2,00 € / 2,00 €
- Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch  
"""
    out = check_for_updates(message, "payload.json", send_on_diff=False)
    assert out == None


def test_check_for_updates_with_diff():
    message = Message()
    message.payload["sections"][2][
        "text"
    ] = """## [Studenten Mensa](https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan)

- Grüne- Thai- Kokos- Gemüsesuppe, Ingwer, Mie-Nudeln, Koriander, Baguettebrot  
2,50 € / 4,30 € / 5,00 €
- Quinoa Bowl - Spinat-Hummus, Brokkoli, Karotten, Ingwer, Casshewkerne  
3,50 € / 5,30 € / 6,00 €
- Chicken Makhani, Basmatireis, Indisches Butterhuhn, Joghurt[Bio], Tomate, Mandeln  
2,50 € / 5,40 € / 6,10 €
- Tagesgericht: Röstkartoffeln, mediterranes Gemüse, Kräuterquark  
3,80 € / 3,80 € / 3,80 €
- . und Hähnchen vom Grill  
2,00 € / 2,00 € / 2,00 €
- Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch  
"""
    out = check_for_updates(message, "payload.json", send_on_diff=False)
    assert out != None


def test_check_for_updates_with_order_and_diff():
    message = Message()
    message.payload["sections"][2][
        "text"
    ] = """## [Studenten Mensa](https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan)

- Grüne- Thai- Kokos- Gemüsesuppe, Ingwer, Mie-Nudeln, Koriander, Baguettebrot  
2,50 € / 4,30 € / 5,00 €
- Quinoa Bowl - Spinat-Hummus, Brokkoli, Karotten, Ingwer, Casshewkerne  
3,50 € / 5,30 € / 6,00 €
- Tagesgericht: Röstkartoffeln, mediterranes Gemüse, Kräuterquark  
3,80 € / 3,80 € / 3,80 €
- Chicken Makhani, Basmatireis, Indisches Butterhuhn, Joghurt[Bio], Tomate, Mandeln  
2,50 € / 5,40 € / 6,10 €
- . und Hähnchen vom Grill  
2,00 € / 2,00 € / 2,00 €
- Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch  
"""
    out = check_for_updates(message, "payload.json", send_on_diff=True)
    assert out != None
