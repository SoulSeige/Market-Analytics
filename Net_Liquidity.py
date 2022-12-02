#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 11:29:14 2022

@author: kgupta
"""
import requests
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Months_History = 6 #How many months history you want to look into (max 4)
#TGA data not available before 18th April 2022. Max call of 100 data points

#Defining Functions
def Treasury_Assets(months):
    today = datetime.date.today()
    start_date=today - datetime.timedelta(months*30)
    start_date = start_date.strftime("%Y-%m-%d")
    url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1?filter=record_date:gte:{},account_type:eq:Treasury%20General%20Account%20(TGA)%20Closing%20Balance&fields=record_date,open_today_bal'\
            .format(start_date)

    page = requests.get(url)
    data = page.json()['data']
    df = pd.DataFrame(data)
    return df

#Defining Functions
def Treasury_Assets2():
    url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/dts_table_1?filter=account_type:eq:Treasury%20General%20Account%20(TGA)%20Closing%20Balance&fields=record_date,open_today_bal'

    page = requests.get(url)
    data = page.json()['data']
    df = pd.DataFrame(data)
    return df

def Reverse_Repo(months):
    today = datetime.date.today()
    start_date=today - datetime.timedelta(months*30)
    start_date = start_date.strftime("%Y-%m-%d")
    url = 'https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?startDate={}'\
            .format(start_date)

    page = requests.get(url)
    data = page.json()['repo']['operations']
    df = pd.DataFrame(data)
    return df

def WALCL():
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=WALCL'
    df = pd.read_csv(url)
    return df

def SP500(months):
    today = datetime.date.today()
    start_date=today - datetime.timedelta(months*30)
    start_date = start_date.strftime("%Y-%m-%d")
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500&cosd={}'\
            .format(start_date)
    df = pd.read_csv(url)
    return df


tga2 = Treasury_Assets2()
#Importing Data:
tga = Treasury_Assets(Months_History).set_index('record_date')
rr = Reverse_Repo(Months_History).set_index('operationDate')
rr=rr[['totalAmtAccepted']].replace(0, np.nan).dropna()
fed = WALCL().set_index('DATE')
sp500 = SP500(Months_History).set_index('DATE')


#Formatting Data:
output = pd.concat([tga,fed,sp500,rr], axis=1)
output.loc[:,['WALCL']] = output.loc[:,['WALCL']].ffill()
output.dropna(inplace=True)
output = output.astype(float)
output['FED'] = output.WALCL * 1000 * 1000
output['TGA'] = output.open_today_bal * 1000 * 1000
output['RR'] = output.totalAmtAccepted


#Calculating Target Cariables:
output['Net_Liquidity'] = output.FED-output.TGA-output.RR
output["Chg_Net_Liquidity"] = output.Net_Liquidity - output.Net_Liquidity.shift(1)
output["SP_FV"] = output.Net_Liquidity / 1000 / 1000 / 1000 / 1.1 - 1625


#Exporting Output to Excel:
output = output[["FED","TGA","RR","Net_Liquidity","Chg_Net_Liquidity", "SP500", "SP_FV"]]

output.to_excel("Net_Liquidity.xlsx")


fig, ax = plt.subplots()
ax2 = ax.twinx()

output_week = output
output_week.index = pd.to_datetime(output_week.index)
output_week = output_week.resample('W-MON').sum()

ax.bar(output_week.index,output_week.Chg_Net_Liquidity/1000000000)
ax.set_ylabel("Change in Net Liquidity in Billions of $")
ax2.plot(output.index,output.SP500, color='orange')
ax2.set_ylabel("S&P 500")
ax.tick_params(axis='x', rotation=30)

print(output.Net_Liquidity[-1]-output.Net_Liquidity[0])


    