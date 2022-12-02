#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:00:07 2022

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

n = 200 #How many datapoints to request from API: minimum of current day - earliest start day + 30
start_date = '2022-04-01' #start date in YYYY-MM-DD format
end_date = '2022-06-30' #end date in YYYY-MM-DD format
volume_type = 'top_tier_volume_total'#'cccagg_volume_total' or top_tier_volume_total'

exchanges = ['Binance', 'FTX', 'Bitstamp', 'Okex', 'Huobipro', 'Bitfinex', 'Lmax']


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
    plt.plot(Data['Date'],Data[ex])
    plt.xticks(rotation=45)
    plt.ylabel("XRP Volume in Dollars")
    plt.xlabel("Date")
    plt.title("Evolution of XRP volumes on "+ ex)


#Plot Area Graph
plt.figure()
plt.stackplot(Data.Date, Data.Binance, Data.FTX, Data.Bitstamp, Data.Okex, Data.Huobipro, Data.Bitfinex, Data.Lmax, labels = exchanges)
plt.legend()
plt.xlabel("Date")
plt.ylabel("XRP Volume in Dollars")
plt.title("Evolution of Exchange Market Share in XRP Volumes")
plt.xticks(rotation=45)


#Plot % Area Graph
Pct_Data = Data[["Date"]]
for ex in exchanges:
    Pct_Data[ex] = (Data[ex]*100)/Data.sum(axis=1)

plt.figure()
plt.stackplot(Pct_Data.Date, Pct_Data.Binance, Pct_Data.FTX, Pct_Data.Bitstamp, Pct_Data.Okex, Pct_Data.Huobipro, Pct_Data.Bitfinex, Pct_Data.Lmax, labels = exchanges)
plt.legend(bbox_to_anchor =(1.3,0.75))
plt.xlabel("Date")
plt.ylabel("% of XRP Volume Share")
plt.title("Evolution of Exchange Market Share in XRP Volumes")


plt.figure()
plt.bar(exchanges, Pct_Data.iloc[-1,1:])
plt.xlabel("Exchanges")
plt.ylabel("% of XRP Volume Share")
plt.title("Current Exchanges Market Share of XRP Volumes")

Rolling_Data = Data[["Date"]]
for ex in exchanges:
    Rolling_Data[ex] = Data[ex].rolling(30).mean()
Rolling_Data = Rolling_Data.dropna()
    
Rolling_Pct_Data = Rolling_Data[["Date"]]

for ex in exchanges:
    Rolling_Pct_Data[ex] = (Rolling_Data[ex]*100)/Rolling_Data.sum(axis=1)

plt.figure()
plt.stackplot(Rolling_Pct_Data.Date, Rolling_Pct_Data.Binance, Rolling_Pct_Data.FTX, Rolling_Pct_Data.Bitstamp, Rolling_Pct_Data.Okex, Rolling_Pct_Data.Huobipro, Rolling_Pct_Data.Bitfinex, Rolling_Pct_Data.Lmax, labels = exchanges)
plt.legend(bbox_to_anchor =(1.3,0.75))
plt.xlabel("Date")
plt.ylabel("% of XRP Volume Share")
plt.title("Evolution of Exchange Market Share in 1m rolling XRP Volumes")

