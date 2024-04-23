import requests
from bs4 import BeautifulSoup
import re
import time


def scraping(accounts, symbol, interval):
    while True:
        total_mentions = 0
        for account in accounts:
            response = requests.get(account)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                tweets = soup.find_all('div', {'class': 'css-175oi2r r-16y2uox r-1wbh5a2 r-1ny4l3l'})
                for tweet in tweets:
                    mentions = re.findall(rf'\b{symbol}\b', tweet.text)
                    total_mentions += len(mentions)
        print(f"\"{symbol}\" was mentioned '{total_mentions}' times in the last '{interval}' minutes.")
        time.sleep(interval * 60)  


accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]


symbol = "$TSLA"

interval = 1

scraping(accounts, symbol, interval)

