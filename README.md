# Mensa-Bot
This MS Teams bot parses the menu of the UKSH Bistro, Cafeteria and the Uni Lübeck Mensa

## Requirements

Install tesseract and everything in the requirements.txt.
```
sudo apt install tesseract-ocr
sudo wget https://github.com/tesseract-ocr/tessdata/raw/main/deu.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
pip install -r requirements.txt
```
I recommend using a virtual environment with `python3-venv`.

## Configure and run

Create a .env file with your MS Teams Webhook.
```
WEBHOOK=<secret>
```

And then run it, to send the daily menu to MS Teams.
```
python3 mensa_bot.py
```

I recommend putting it in a crontab with `crontab -e`, e.g. to run it every weekday at 10:30 AM.
```
30 10 * * 1-5 /path/to/python-venv/bin/python3 /path/to/Mensa-Bot/mensa_bot.py > /path/to/log/output.log 2>&1
```

## Thanks

- [@Draculente](https://github.com/Draculente) for the [Mensa-API](https://github.com/Draculente/mensa-api)
- Danielle for the initial Mensa-Bot