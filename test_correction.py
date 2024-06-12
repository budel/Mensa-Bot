from mensa_bot import check_for_updates


MENU_LIST = [
    {
        "title": "MFC Cafeteria",
        "url": "https://www.uksh.de/uksh_media/Speisepl%C3%A4ne/L%C3%BCbeck+_+MFC+Cafeteria/KW+24+Speiseplan+MFC+10_06_2024+_+14_06_2024-p-786753.pdf",
        "items": [
            {
                "name": "Tintenfischringe mit Knoblauchdip, Kräuterbrot am Salatboquet",
                "price": "€6,60 / €8,78\n",
            },
            {
                "name": "Spaghetti mit Tomatensauce, geriebenen Hartkäse dazu ein Beilagensalat",
                "price": "€4,15 / €5,52\n",
            },
            {
                "name": "Köttbullar mit Bratensauce, Mischgemüse dazu Kartoffelstampf und Preiselbeeren",
                "price": "€6,40 / €8,51\n",
            },
        ],
    },
    {
        "title": "UKSH Bistro",
        "url": "https://www.uksh.de/uksh_media/Speisepl%C3%A4ne/L%C3%BCbeck+_+UKSH_Bistro/KW+24+Speiseplan+Bistro+10_06_2024+_+16_06_2024-p-786742.pdf",
        "items": [
            {
                "name": "Putenbruststreifen mit Sour Creme auf Süßkartoffelgemüsepfanne",
                "price": "€6,60 / €8,78\n",
            },
            {
                "name": "Spaghetti mit Tomatensauce, geriebenen Hartkäse dazu ein Beilagensalat",
                "price": "€4,15 / €5,52\n",
            },
            {
                "name": "Köttbullar mit Bratensauce, Mischgemüse dazu Kartoffelstampf und Preiselbeeren",
                "price": "€6,30 / €8,38\n",
            },
            {
                "name": "Tintenfischringe mit Knoblauchdip, Kräuterbrot am Salatboquet",
                "price": "€6,60 / €8,78\n",
            },
        ],
    },
    {
        "title": "Studenten Mensa",
        "url": "https://studentenwerk.sh/de/mensen-in-luebeck?ort=3&mensa=8#mensaplan",
        "items": [
            {
                "name": "Pikante Sesamnudeln, asiatisches Pfannengemüse",
                "price": "2,50 € / 5,35 € / 6,05 €",
            },
            {
                "name": "Börek, Spinatfüllung, Tomaten- Minzsugo, Couscous",
                "price": "2,50 € / 4,50 € / 5,20 €",
            },
            {"name": "Grünes Orzotto, Rucola, Tomaten", "price": ""},
            {
                "name": "Currywurst Hot Pot(t), Karamellisierte Balsamico Zwiebeln, Kartoffelspalten",
                "price": "3,95 € / 5,75 € / 6,45 €",
            },
            {
                "name": "Burger im Menü mit Fritz 0,33l, Chicken Burger, . mit Pommes Frites",
                "price": "6,95 € / 6,95 € / 6,95 €",
            },
            {
                "name": "Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch",
                "price": "",
            },
        ],
    },
    {"title": "Foodtruck", "url": "https://www.street-gourmet.de", "items": []},
]


def test_check_for_updates_without_diff():
    out = check_for_updates(MENU_LIST, "menus.json", send_on_diff=False)
    assert out == None


def test_check_for_updates_with_different_order():
    menu_list = MENU_LIST
    menu_list[2]["items"] = [
        {
            "name": "Pikante Sesamnudeln, asiatisches Pfannengemüse",
            "price": "2,50 € / 5,35 € / 6,05 €",
        },
        {
            "name": "Börek, Spinatfüllung, Tomaten- Minzsugo, Couscous",
            "price": "2,50 € / 4,50 € / 5,20 €",
        },
        {
            "name": "Currywurst Hot Pot(t), Karamellisierte Balsamico Zwiebeln, Kartoffelspalten",
            "price": "3,95 € / 5,75 € / 6,45 €",
        },
        {"name": "Grünes Orzotto, Rucola, Tomaten", "price": ""},
        {
            "name": "Burger im Menü mit Fritz 0,33l, Chicken Burger, . mit Pommes Frites",
            "price": "6,95 € / 6,95 € / 6,95 €",
        },
        {
            "name": "Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch",
            "price": "",
        },
    ]
    out = check_for_updates(menu_list, "menus.json", send_on_diff=False)
    assert out == None


def test_check_for_updates_with_diff():
    menu_list = MENU_LIST
    menu_list[2]["items"] = [
        {
            "name": "Milde Sesamnudeln, asiatisches Pfannengemüse",
            "price": "2,50 € / 5,35 € / 6,05 €",
        },
        {
            "name": "Börek, Spinatfüllung, Tomaten- Minzsugo, Couscous",
            "price": "2,50 € / 4,50 € / 5,20 €",
        },
        {
            "name": "Currywurst Hot Pot(t), Karamellisierte Balsamico Zwiebeln, Kartoffelspalten",
            "price": "3,95 € / 5,75 € / 6,45 €",
        },
        {
            "name": "Burger im Menü mit Fritz 0,33l, Chicken Burger, . mit Pommes Frites",
            "price": "6,95 € / 6,95 € / 6,95 €",
        },
        {
            "name": "Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch",
            "price": "",
        },
    ]
    out = check_for_updates(menu_list, "menus.json", send_on_diff=False)
    assert out != None


def test_check_for_updates_with_order_and_diff():
    menu_list = MENU_LIST
    menu_list[2]["items"] = [
        {
            "name": "Milde Sesamnudeln, asiatisches Pfannengemüse",
            "price": "2,50 € / 5,35 € / 6,05 €",
        },
        {
            "name": "Currywurst Hot Pot(t), Karamellisierte Balsamico Zwiebeln, Kartoffelspalten",
            "price": "3,95 € / 5,75 € / 6,45 €",
        },
        {
            "name": "Börek, Spinatfüllung, Tomaten- Minzsugo, Couscous",
            "price": "2,50 € / 4,50 € / 5,20 €",
        },
        {
            "name": "Burger im Menü mit Fritz 0,33l, Chicken Burger, . mit Pommes Frites",
            "price": "6,95 € / 6,95 € / 6,95 €",
        },
        {
            "name": "Zu jedem wechselnden Tagesgericht gibt es ein Fritz-Getränk zum Aktionspreis von 1,60€ dazu !, Wir freuen uns auf Euch",
            "price": "",
        },
    ]
    out = check_for_updates(menu_list, "menus.json", send_on_diff=False)
    assert out != None
