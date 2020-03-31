#!/usr/bin/env python3

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
#import ast
import notify2
import time

APP_NAME = "Tradepy"
coins_id = [1, 2, 52, 1027, 1720]
credit_count = 0

def get_coins_info(data):
    #dict = ast.literal_eval(data)
    credit_count = data.get("status").get("credit_count")
    print(str(credit_count))
    dict = data.get("data")
    coins = []
    for id in coins_id:
        coins.append(dict.get(str(id)))
    coins = sorted(coins, key=lambda k: k["quote"]["USD"]["percent_change_1h"], reverse=True)
    return coins

def generate_text(coins):
    text = ""
    delimiter = "\n"
    title =  "{}: {:.2f}$ ({:.2f}%)".format(coins[0].get("name"), coins[0].get("quote").get("USD").get("price"), coins[0].get("quote").get("USD").get("percent_change_1h"))
    for coin in coins[1:]:
        text += "{}: {:.2f}$ ({:.2f}%){}".format(coin.get("name"), coin.get("quote").get("USD").get("price"), coin.get("quote").get("USD").get("percent_change_1h"), delimiter)

    return title, text

def notify(title, text):
    notify2.init(APP_NAME)
    notification = notify2.Notification(APP_NAME, None, APP_NAME)
    notification.set_urgency(notify2.URGENCY_NORMAL)
    notification.set_timeout(5000)
    notification.update(title, text)
    notification.show()

def main():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'id':'1,2,52,328,1027,1720'
    }
    # ['Bitcoin': 1, 'Litecoin': 2, 'XRP': 52, 'Monero': 328, 'Etherum': 1027, 'IOTA': 1720]

    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    }

    session = Session()
    session.headers.update(headers)

    while True:
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            coins = get_coins_info(data)
            title, text = generate_text(coins)
            notify(title, text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        time.sleep(300)

main()
