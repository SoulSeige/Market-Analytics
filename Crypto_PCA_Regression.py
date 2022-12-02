#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:53:13 2022

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
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression

n=100
asset = "btc"

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
    df['Date'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def daily_volume_historical(symbol, comparison_symbol, limit=300):
    url = 'https://min-api.cryptocompare.com/data/symbol/histoday?fsym={}&tsym={}&limit={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def PCA_asset_df(slug):
    asset_volumes = daily_volume_historical(slug, 'USD', limit = n)
    asset = daily_price_historical("XRP", "USD", limit = n)
    asset["volume"] = asset_volumes['top_tier_volume_total']
    asset["returns"] = asset.close.pct_change()
    asset["HML"] = asset.high - asset.low
    asset["VMOM"] = (asset.close -asset.close.shift(periods=7)) / asset.HML.rolling(22).mean()
    asset['IV'] = np.where(asset.open<asset.close,(np.log(asset.low/asset.high))**2,(np.log(asset.high/asset.low))**2)
    asset = asset[["Date","volume","returns", "HML", "VMOM","IV"]].dropna()
    asset.set_index("Date", inplace =True)
    
    return asset


xrp = PCA_asset_df('xrp')
crypto = PCA_asset_df(asset)

crypto=(crypto-crypto.mean())/crypto.std()

pca = PCA(n_components=3)
pca.fit(crypto)

pc1 = crypto * pca.components_[0]
pc1 = pc1.sum(axis=1)

pc2 = crypto * pca.components_[1]
pc2 = pc2.sum(axis=1)

pc3 = crypto * pca.components_[2]
pc3 = pc3.sum(axis=1)

X = pd.DataFrame({"pc1":pc1, "pc2":pc2, "pc3":pc3})


split = datetime.datetime(2022,7,15,0,0,0)
Xtrain = X[split:]
Xtest = X[:split]

xrptrain = xrp[split:]
xrptest = xrp[:split]

reg = LinearRegression().fit(Xtrain,xrptrain.returns)
ypred = reg.predict(Xtest)


plt.plot(xrptest.index,xrptest.returns)
plt.plot(xrptest.index, ypred)

plt.xticks(rotation=45)
print(pca.components_)
print(pca.explained_variance_ratio_)