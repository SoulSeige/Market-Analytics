#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 15:29:33 2022

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
from matplotlib.ticker import StrMethodFormatter
import yfinance as yf
from IPython.display import display

n = 100 #How many datapoints to request from API: minimum of current day - earliest start day + 30
start_date = '2022-04-01' #start date in YYYY-MM-DD format
end_date = '2022-06-30' #end date in YYYY-MM-DD format
volume_type = 'top_tier_volume_total'#'cccagg_volume_total' or top_tier_volume_total'

#exchanges = ['Binance','HuobiPro','Upbit', 'Bithumb', 'FTX', 'HitBTC', 'Bitstamp', 'DigiFinex']
exchanges = ['Binance', 'FTX']


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

#################################################################################################################################################

exchanges = ['Binance', 'FTX', 'HitBTC', 'Bitstamp', 'DigiFinex']

symb = 'USDT'

Data = daily_price_historical('xrp', symb, limit = n, exchange='binance')
price = daily_price_historical('xrp','USD', limit=n)

Data = Data[["time"]]

for ex in exchanges:
        temp = daily_price_historical('xrp', symb, limit = n, exchange=ex)
        Data[ex] = (temp['volumefrom']*price['close']) +(temp['volumeto'])

Data.set_index('time', inplace=True)
Data.to_excel("XRP_USDT_Volume_History.xlsx")

#################################################################################################################################################

exchanges = ['Binance',"HuobiPro","Kucoin","OKEX"]

symb = 'USDC'

Data = daily_price_historical('xrp', symb, limit = n, exchange=exchanges[0])
price = daily_price_historical('xrp','USD', limit=n)

Data = Data[["time"]]

for ex in exchanges:
        temp = daily_price_historical('xrp', symb, limit = n, exchange=ex)
        Data[ex] = (temp['volumefrom']*price['close']) +(temp['volumeto'])

Data.set_index('time', inplace=True)
Data.to_excel("XRP_USDC_Volume_History.xlsx")

#################################################################################################################################################

exchanges = ['Bitstamp','Bitfinex','Kraken','lmax','IndependentReserve']

symb = 'USD'

Data = daily_price_historical('xrp', symb, limit = n, exchange=exchanges[0])
price = daily_price_historical('xrp','USD', limit=n)

Data = Data[["time"]]

for ex in exchanges:
        temp = daily_price_historical('xrp', symb, limit = n, exchange=ex)
        Data[ex] = (temp['volumefrom']*price['close']) +(temp['volumeto'])

Data.set_index('time', inplace=True)
Data.to_excel("XRP_USD_Volume_History.xlsx")