#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 14:11:28 2019

@author: sinsakuokazaki
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("ORCL.csv")

#function for trade bollinger
def tradeBollinger(year, w, k):
    sds = df.loc[df['Year'] == year]['Adj Close'].rolling(window=w, min_periods=1).std()
    mas = df.loc[df['Year'] == year]['Adj Close'].rolling(window=w, min_periods=1).mean()
    adj_closes = df.loc[df['Year'] == year]['Adj Close']
    own_stock = False
    gains = np.array([])
    losses = np.array([])
    for ma, sd, adj in zip(mas, sds, adj_closes):
        if adj > ma + k * sd:
            if adj <= 100:
                stock_owned = 100 // adj
                bid = adj
                own_stock = True
                
        elif own_stock and adj < ma - k * sd:
            sell = adj * stock_owned
            profit = sell - bid
            own_stock = False
            if profit > 0:
                gains = np.append(gains, profit)
            elif profit < 0:
                losses = np.append(losses, profit)
    return gains, losses

#function to get average of gain 
def getAveGain(gains):
    if gains.size != 0:
        ave_gain = np.mean(gains)
    else: ave_gain = None
    return ave_gain

#function  to get average of loss
def getAveLoss(losses):
    if losses.size != 0:
        ave_loss = np.mean(losses)
    else: ave_loss = None
    return ave_loss
#list of ks and ws  
ks = np.linspace(5, 35, 5) / 10
ws = list(range(10, 110, 10))

#obtain dictionary of gain and loss and create dataframe
gain_dict = {'W': ws}
loss_dict = {'W': ws}
for k in ks:
    gain_list = []
    loss_list = []
    for w in ws:
        gains, losses = tradeBollinger(2018, w, k)
        ave_gain = getAveGain(gains)
        ave_loss = getAveLoss(losses)
        gain_list.append(ave_gain)
        loss_list.append(ave_loss)
    gain_dict[k] = gain_list
    loss_dict[k] = loss_list    
df_gain = pd.DataFrame(data=gain_dict).fillna(0.0)
df_gain = df_gain.set_index("W")
df_loss = pd.DataFrame(data=loss_dict).fillna(0.0)
df_loss = df_loss.set_index("W")

#prepare for the data visualization
def prepData(df):
    data = np.array([])
    for w in df.index:
        data = np.append(data, df.loc[w])
    return data
#prepare for the axis of visualization
def prepAxis(df):
    index = list(df.index)
    column = list(df.columns)
    x = []
    for i in index:
        for c in range(len(column)):
            x.append(i)
    y = column * len(index)
    return x, y

gain_data = prepData(df_gain)
loss_data = prepData(df_loss)
gain_x, gain_y = prepAxis(df_gain)
loss_x, loss_y = prepAxis(df_loss)

#visualiza
plt.figure(figsize=(7,7))
plt.xticks(gain_x)
plt.yticks(gain_y)
plt.scatter(gain_x, gain_y, s = gain_data * 20, color = 'g', alpha = 0.5)
plt.scatter(loss_x, loss_y, s = loss_data * -20, color = 'r', alpha = 0.5 )
plt.xlabel('W', fontsize=18)
plt.ylabel('k', fontsize=18)
plt.show()