# discord_crypto_price_bot
Cryptocurrencies Price Bot with Chart for Discord. Support every coin listed on CoinGecko.

## Installation
- Install Python.
- Clone this repo.
- Head over to [Discord Dev Portal](https://discord.com/developers/applications), create a new bot and get a token.
- Set "Send Messages" and "Attach Files" permissions.
- Create a .env file in the project root folder, and fill it with that:
```
DISCORD_TOKEN=your_discord_token
```
- Create a new virtual env and activate it:
```
python -m venv venv
source venv/bin/activate
```
- Install requirements:
```
pip install -r requirements.txt
```
- You can launch the bot and add it to your Discord server:
```
python main.py
```
