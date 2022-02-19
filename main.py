import discord
from utils import nickname_generator, get_random_image, cg, format_crypto_data, get_currency, search_coin, draw_chart
from vars import bull_beg, bull_mid, bull_end
from discord.ext import commands
import io
from PIL import Image
import random


# globals vars
TOKEN = "OTI5ODIzNzQ3NzMxNTE3NDUx.Yds72A.2gh3aDqg3aGdC51BSVbhHtdFmpg"
award_id = 192352519534411777
coins_list = cg.get_coins_list()


# Initialize Bot and Denote The Command Prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",  intents=intents)


# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


# Fun commands

@bot.command()
@commands.has_permissions(change_nickname=True)
async def virg(ctx):
    """
    Poste un nom marrant + une image marrante
    """
    nickname = nickname_generator()
    if len(nickname) <= 32:
        award = await ctx.message.guild.query_members(user_ids=[award_id])
        award = award[0]
        await award.edit(nick=nickname)
    img = discord.File(get_random_image('award'))
    await ctx.send(nickname, file=img)


@bot.command()
@commands.has_permissions(change_nickname=True)
async def name(ctx):
    """
    Poste un nom marrant et change le pseudal de Renaud
    """
    nickname = nickname_generator()
    if len(nickname) <= 32:
        award = await ctx.message.guild.query_members(user_ids=[award_id])
        award = award[0]
        await award.edit(nick=nickname)
    await ctx.send(nickname)


@bot.command()
async def fun(ctx):
    """
    Poste l'une des innombrables images marrantes de Renaud
    """
    img = discord.File(get_random_image('award'))
    await ctx.send(file=img)


@bot.command()
async def jap(ctx):
    """
    Poste l'un des drapeaux du japon
    """
    img = discord.File(get_random_image('japon'))
    await ctx.send(file=img)


# Crypto-related commands

@bot.command()
async def price(ctx, *args):
    # loading message
    await ctx.send("""**La Virg'** exauce ton souhait...""")

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
            award_img = discord.File(get_random_image('cg/dump'))
            award_comment = """\n**Bon, le bearmarket... *'remonte son fute, commence a chialer'***"""
            emoji = random.choice(["🚨", "📉", "🕎", "✡", "🚬", "🖕", "💀", "💩", "👎", "😨", "🐌", "🐒", "🦐", "🌪️"])
        else:
            # Bull
            award_img = discord.File(get_random_image('cg/pump'))
            award_comment = f"""\n**{random.choice(bull_beg)}, {random.choice(bull_mid)}... *'{random.choice(bull_end)}'***"""
            emoji = random.choice(["🚀", "🤙", "💸", "🔥", "👌", "📈", "🤘", "👍", "🧠", "👀", "🍆", "🤑", "💰", "🤌", "💪", "🦍", "💦", "☄️"])

        bot_resp = f"> **{args[0].upper()}**" + \
                   f"\n\n• Price: **{format_crypto_data(str((price)))} {currency[1]}**" + \
                   f"\n• Market Cap: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_market_cap'], 2)))} {currency[1]}**" + \
                   f"\n• 24h Volume: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_24h_vol'], 2)))} {currency[1]}**" + \
                   f"\n• 24h Change: **{format_crypto_data(str(round(data[coin][f'{currency[0]}_24h_change'], 3)))} %**  {emoji}" + \
                   f"\n{award_comment}"

        # drawing chart
        image_data = draw_chart(coin, "1", currency[0])
        image = Image.open(io.BytesIO(image_data))
        arr = io.BytesIO()
        image.save(arr, format='png')
        arr.seek(0)
        await ctx.send(bot_resp, file=discord.File(fp=arr, filename="chart.png"))
        await ctx.send(file=award_img)

    except KeyError:
        bot_resp = "T'es sûr d'avoir bien écrit le nom du coin, connard ?"
        award_img = discord.File('imgs/cg/404.jpg')
        await ctx.send(bot_resp, file=award_img)

    except TypeError:
        bot_resp = "L'Oracle a rencontré une erreur..."
        award_img = discord.File('imgs/cg/error.png')
        await ctx.send(bot_resp, file=award_img)


@bot.command()
async def chart(ctx, coin, days):

    await ctx.send("""**La Virg'** invoque la Sainte Charte...""")

    try:
        coin = search_coin(coin, coins_list)
        image_data = draw_chart(coin, days, "usd")

        image = Image.open(io.BytesIO(image_data))
        arr = io.BytesIO()
        image.save(arr, format='png')
        arr.seek(0)

        await ctx.send(file=discord.File(fp=arr, filename="chart.png"))

    except KeyError:
        bot_resp = "T'es sûr d'avoir bien écrit le nom du coin, connard ?"
        award_img = discord.File('imgs/cg/404.jpg')
        await ctx.send(bot_resp, file=award_img)

    except TypeError:
        bot_resp = "L'Oracle a rencontré une erreur..."
        award_img = discord.File('imgs/cg/error.png')
        await ctx.send(bot_resp, file=award_img)


# Errors handling

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        bot_resp = "**La Virg'** ne peux pas invoquer la chart si tu ne précises pas de coin / de jours." + \
                   "\nRappel: **!chart <coin> <days>**"
        award_img = discord.File('imgs/cg/404.jpg')
        await ctx.send(bot_resp, file=award_img)

    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("**La Virg'** ne peux pas répondre à une telle hérésie. Connard.")


bot.run(TOKEN)

