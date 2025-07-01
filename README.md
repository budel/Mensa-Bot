# Mensa-Bot
This MS Teams bot parses the menu of the UKSH Bistro, Cafeteria and the Uni Lübeck Mensa

## Requirements

Start dev shell using nix
```
nix develop
```

## Configure and run

Create a .env file with your MS Teams Webhook.
```
WEBHOOK=<secret>
```

Parse this and the next week using
```
python3 parse_week.py
```

And then send the daily menu to MS Teams.
```
python3 mensa_bot.py
```
It fetches the last week from github.io.

Two github actions, configured in `.github/workflows/` do exactly that.

## Thanks

- [@Draculente](https://github.com/Draculente) for the [Mensa-API](https://github.com/Draculente/mensa-api)
- Danielle for the initial Mensa-Bot
