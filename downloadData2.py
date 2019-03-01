#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:19:33 2019

@author: sinsakuokazaki
"""

from pandas_datareader import data as web
import os
import math
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def get_stock(ticker, start_date, end_date, s_window, l_window):
    try:
        df = web.get_data_yahoo(ticker, start=start_date, end=end_date)
        df['Return'] = df['Adj Close'].pct_change()
        df['Return'].fillna(0, inplace = True)
        df['Date'] = df.index
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year 
        df['Day'] = df['Date'].dt.day
        for col in ['Open', 'High', 'Low', 'Close', 'Adj Close']:
            df[col] = df[col].round(2)
        df['Weekday'] = df['Date'].dt.weekday_name  
        df['Short_MA'] = df['Adj Close'].rolling(window=s_window, min_periods=1).mean()
        df['Long_MA'] = df['Adj Close'].rolling(window=l_window, min_periods=1).mean()        
        col_list = ['Date', 'Year', 'Month', 'Day', 'Weekday', 'Open', 
                    'High', 'Low', 'Close', 'Volume', 'Adj Close',
                    'Return', 'Short_MA', 'Long_MA']
        df = df[col_list]
        return df
    except Exception as error:
        print(error)
        return None

def get_last_digit(y):
        x = str(round(float(y),2))
        x_list = x.split('.')
        fraction_str = x_list[1]
        if len(fraction_str)==1:
            return 0
        else:
            return int(fraction_str[1])


ticker='KO'
start_date='2014-01-01'
end_date='2018-12-31'
s_window = 14
l_window = 50
input_dir = r'/Users/sinsakuokazaki/Document/DataScience'
output_file = os.path.join(input_dir, ticker + '.csv')

df = get_stock(ticker, start_date, end_date, s_window, l_window)
df['last digit'] = df['Open'].apply(get_last_digit)

df['count'] = 1
total = len(df)

df_1 = df.groupby(['last digit'])['count'].sum()
df_2 = df_1.to_frame()
df_2.reset_index(level=0, inplace=True)
df_2['digit_frequency'] = df_2['count']/total
df_2['uniform'] = 0.10

output_file = os.path.join(input_dir, ticker + '_digit_analysis.csv')
df_2.to_csv(output_file, index=False)

