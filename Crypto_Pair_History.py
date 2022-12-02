#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:56:39 2022

@author: kgupta
"""

#importing libraries
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

assets = ['USD','EUR','JPY','BTC', 'USDT', 'USDC', 'BUSD']

n = 240


def Pair_History(symbol, comparison_symbol, limit=300, aggregate=1):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    page = requests.get(url)
    data = page.json()['Data']['Data']
    df = pd.DataFrame(data)
    df['time'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    df['time'] = df["time"] = pd.to_datetime(df["time"]).dt.date
    return df

def daily_price_historical(symbol, comparison_symbol, all_data=False, limit=10, aggregate=1, exchange=''):
    
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
        
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['time'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    df['time'] = df["time"] = pd.to_datetime(df["time"]).dt.date
    return df

Data = Pair_History('XRP', 'BTC', limit = n)[['time']]

#volume from = amount of XRP traded into asset
#volume to = amount of asset traded into XRP

for asset in assets:
    temp = Pair_History('XRP', asset, limit = n)
    Data[asset + 'to'] = temp['volumeto']
    Data[asset + 'from'] = temp['volumefrom']



Rolling_Data = Data[["time"]]

for asset in assets:
    Rolling_Data[asset + 'to'] = Data[asset + 'to'].rolling(30).mean()
    Rolling_Data[asset + 'from'] = Data[asset + 'from'].rolling(30).mean()

Rolling_Data = Rolling_Data.dropna()



for asset in assets:
    fig, ax = plt.subplots()
    ax.plot(Rolling_Data['time'],Rolling_Data[asset + 'from'],label='XRP to '+asset)
    ax.plot(Rolling_Data['time'],Rolling_Data[asset + 'to'], label=asset +' to XRP')
    plt.legend()
    plt.title("XRP/" + asset + " Rolling 1m Volume")
    plt.xlabel("Date")
    plt.ylabel("Volume in Base Currency")
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.xticks(rotation=45)
    plt.savefig("XRP_" + asset+'.jpeg', dpi=1200, bbox_inches='tight')