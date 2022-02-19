import random
import plotly.graph_objects as go
from plotly.graph_objects import Layout
from datetime import datetime
from os import listdir
from os.path import isfile, join
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()


def get_random_image(path):
    imgs = [f for f in listdir(f'imgs/{path}/') if isfile(join(f'imgs/{path}/', f))]
    return f'imgs/{path}/{random.choice(imgs)}'


# Price utils
def get_currency(cur):
    if "eur" in cur:
        currency = ['eur', '€']
    else:
        currency = ['usd', '$']
    return currency


def search_coin(coin, coins_list):
    coin = str(coin).lower()
    if coin == "btc" or coin == "bitcoin":
        coin = "bitcoin"
    else:
        for item in coins_list:
            if coin == item['symbol'].lower() or coin == item['name'].lower():
                coin = item['id']
    return coin


def format_crypto_data(data: str) -> str:
    if '.' in data:
        number = ' '.join([data.split('.')[0][::-1][i:i+3] for i in range(0, len(data.split('.')[0]), 3)])
        decimals = data.split('.')[1]
    else:
        number = ' '.join([data[::-1][i:i + 3] for i in range(0, len(data.split('.')[0]), 3)])
        decimals = '00'
    return f'{number[::-1]}.{decimals}'


def draw_chart(coin, days, cur):

    if days == "1":
        title = f"{coin.upper()}: 24h Chart"
    else:
        title = f"{coin.upper()}: {days} Days Chart ({cur})"

    cg_data = cg.get_coin_market_chart_by_id(id=coin, vs_currency=cur, days=days)
    x_time = []
    y_price = []

    for data in cg_data['prices']:
        x_time.append(datetime.utcfromtimestamp(float(data[0] / 1000)))
        y_price.append(data[1])

    layout = Layout(
        paper_bgcolor='#36393f',
        autosize=False,
        title=title,
        font={
            "size": 18,
            "color": "white",
        }
    )

    fig = go.Figure(
        [go.Scatter(x=x_time, y=y_price)],
        layout=layout
    )

    fig.update_yaxes(
        automargin=True,
        color="white"
    )
    fig.update_xaxes(
        automargin=True,
        color="white"
    )

    fig.update_layout(
        title={
            'y': 0.9,  # new
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'  # new
        }
    )
    return fig.to_image(format="jpg")
