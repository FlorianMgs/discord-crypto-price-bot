import discord
from dotenv import load_dotenv
from utils import get_random_image, cg, format_crypto_data, get_currency, search_coin, draw_chart
from discord.ext import commands
import io
import os
from PIL import Image

# globals vars
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
coins_list = cg.get_coins_list()


# Initialize Bot and Denote The Command Prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",  intents=intents)


# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


# Crypto-related commands

@bot.command()
async def price(ctx, *args):
    # loading message
    await ctx.send("""**The Oracle** is gathering data...""")

    # getting currency
    currency = get_currency(args)

    # searching coin
    coin = search_coin(args[0], coins_list)

    # gathering data
    data = cg.get_price(ids=coin, vs_currencies=currency[0], include_market_cap='true', include_24hr_vol='true', include_24hr_change='true')

    # creating response
    try:
        if "e" in str(data[coin][currency[0]]):
            price = format(data[coin][currency[0]], '.8f')
        else:
            price = data[coin][currency[0]]

        if data[coin][f'{currency[0]}_24h_change'] < 0:
            # Bear
            img = discord.File(get_random_image('cg/dump'))
        else:
            # Bull
            img = discord.File(get_random_image('cg/pump'))
        bot_resp = f"> **{args[0].upper()}**" + \
                   f"\n\n• Price: **{format_crypto_data(str((price)))} {currency[1]}**" + \
                   f"\n• Market Cap: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_market_cap'], 2)))} {currency[1]}**" + \
                   f"\n• 24h Volume: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_24h_vol'], 2)))} {currency[1]}**" + \
                   f"\n• 24h Change: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_24h_change'], 3)))} %**"

        # drawing chart
        image_data = draw_chart(coin, "1", currency[0])
        image = Image.open(io.BytesIO(image_data))
        arr = io.BytesIO()
        image.save(arr, format='png')
        arr.seek(0)
        await ctx.send(bot_resp, file=discord.File(fp=arr, filename="chart.png"))
        await ctx.send(file=img)

    except KeyError:
        bot_resp = "Are you sure you spelled the coin name correctly ?"
        await ctx.send(bot_resp)

    except TypeError:
        bot_resp = "**The Oracle** has encountered an error..."
        img = discord.File('imgs/cg/error.png')
        await ctx.send(bot_resp, file=img)


@bot.command()
async def chart(ctx, coin, days):

    await ctx.send("""**The Oracle** is getting the chart...""")

    try:
        coin = search_coin(coin, coins_list)
        image_data = draw_chart(coin, days, "usd")

        image = Image.open(io.BytesIO(image_data))
        arr = io.BytesIO()
        image.save(arr, format='png')
        arr.seek(0)

        await ctx.send(file=discord.File(fp=arr, filename="chart.png"))

    except KeyError:
        bot_resp = "Are you sure you spelled the coin name correctly ?"
        await ctx.send(bot_resp)

    except TypeError:
        bot_resp = "**The Oracle** has encountered an error..."
        img = discord.File('imgs/cg/error.png')
        await ctx.send(bot_resp, file=img)


# Errors handling

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        bot_resp = "**The oracle** can't invoke the chart if you don't specify coin name/days." + \
                   "\nCommand: **!chart <coin> <days>**"
        img = discord.File('imgs/cg/404.jpg')
        await ctx.send(bot_resp, file=img)

    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Invalid command.")


bot.run(TOKEN)

