#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:55:08 2022

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

n = 240 #How many datapoints to request from API: minimum of current day - earliest start day + 30
start_date = '2022-04-01' #start date in YYYY-MM-DD format
end_date = '2022-06-30' #end date in YYYY-MM-DD format
volume_type = 'top_tier_volume_total'#'cccagg_volume_total' or top_tier_volume_total'

exchanges = ['Binance', 'Bithumb', 'HitBTC', 'bitcoincom','HuobiPro']

def daily_volume_historical(symbol, comparison_symbol, limit=300):
    url = 'https://min-api.cryptocompare.com/data/symbol/histoday?fsym={}&tsym={}&limit={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

#CryptoCompare API: historical price data
def daily_volume_symbexch(symbol, comparison_symbol, all_data=False, limit=10, exchange='CCCAGG'):
    url = 'https://min-api.cryptocompare.com/data/exchange/symbol/histoday?fsym={}&tsym={}&limit={}&e={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, exchange.upper())
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df




Data = daily_volume_symbexch('xrp', 'USD', limit = n, exchange='ftx')
Data["Date"] = pd.to_datetime(Data["timestamp"]).dt.date
Data = Data[["Date"]]


for ex in exchanges:
        temp = daily_volume_symbexch('xrp', 'USD', limit = n, exchange=ex)
        Data[ex] = temp['volumetotal']


Rolling_Data = Data[["Date"]]

for ex in exchanges:
    Rolling_Data[ex] = Data[ex].rolling(30).mean()
Rolling_Data = Rolling_Data.dropna()

"""
#Plot line graphs (Overlapping)
for ex in exchanges:
    #plt.figure()
    plt.plot(Data['Date'],Data[ex],label=ex)
plt.xticks(rotation=45)
plt.ylabel("XRP Volume in Dollars")
plt.xlabel("Date")
plt.title("Evolution of XRP volumes on exchanges")
plt.legend()
plt.ticklabel_format(style='plain',axis='y')
loc, labels = plt.yticks()



#Plot line graphs (Individual)
for ex in exchanges:
    plt.figure()
    plt.plot(Rolling_Data['Date'],Rolling_Data[ex])
    plt.xticks(rotation=45)
    plt.ylabel("XRP Volume in Dollars")
    plt.xlabel("Date")
    plt.title("Evolution of 1m rolling XRP volumes on " + ex)
"""

volumes = daily_volume_historical('xrp', 'USD', limit = n)
Data['Sum']=Data.sum(axis=1)
Data['Total'] = volumes['top_tier_volume_total']
Data['Pct_of_Total']= Data['Sum']*100/Data['Total']
Data['Pct_of_Total'] = Data['Pct_of_Total'].rolling(30).mean()

fig, ax = plt.subplots()
ax.plot(Data['Date'],Data['Pct_of_Total'])

plt.ylabel("% of Total XRP Volume")
plt.xlabel("Date")
plt.title("Evolution of XRP volumes on exchanges")
plt.xticks(rotation=30)
plt.title("Top 5 exchanges contribution to total xrp volume")
plt.savefig('chart.jpeg', dpi=1200, bbox_inches='tight')