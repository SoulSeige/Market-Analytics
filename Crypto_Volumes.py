#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:18:38 2022

@author: kgupta
"""
import requests
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, zscore
import matplotlib.pyplot as plt
import yfinance as yf
from IPython.display import display
from matplotlib.ticker import StrMethodFormatter

cryptos = ['BTC','ETH', 'ADA', 'AVAX', 'SOL', 'BNB']
n = 14 #How many datapoints to request from API: minimum of current day - earliest start day + 30
start_date = '2020-07-26' #start date in YYYY-MM-DD format
end_date = '2022-07-26' #end date in YYYY-MM-DD format
volume_type = 'top_tier_volume_total'#'cccagg_volume_total' or top_tier_volume_total'


def daily_volume_historical(symbol, comparison_symbol, limit=300):
    url = 'https://min-api.cryptocompare.com/data/symbol/histoday?fsym={}&tsym={}&limit={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df



volumes = daily_volume_historical('XRP', 'USD', limit = n)


fig, ax = plt.subplots()
ax.plot(volumes.timestamp,volumes[volume_type])
plt.xticks(rotation=45)
plt.ylabel("XRP Volume in Dollars")
plt.xlabel("Date")
plt.title("Evolution of XRP volumes")
ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
plt.savefig('XRP_Volume_Hist.jpeg', dpi=1200, bbox_inches='tight')

"""
volumes = volumes[['timestamp',volume_type]]
volumes = volumes.rename(columns={"timestamp": "Date", volume_type: "XRP"})
volumes["Date"] = pd.to_datetime(volumes["Date"]).dt.date


for crypto in cryptos:
    Data = daily_volume_historical(crypto, 'USD', limit = n)
    volumes[crypto] = Data[volume_type]

#volumes.to_excel('Crypto_Volumes.xlsx')
"""