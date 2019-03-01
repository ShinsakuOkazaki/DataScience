#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 19:46:45 2019

@author: sinsakuokazaki
"""

#If adj close > s_ma then buy 
#Else sell


import os
#Get file
ticker = "ORCL"
input_dir = r'/Users/sinsakuokazaki/Document/DataScience'
output_file = os.path.join(input_dir, ticker + '.csv')
with open(output_file) as f:
    lines = f.read().splitlines()

#break one string into elements of string
for row in range(len(lines)):
    lines[row] = lines[row].split(",")
    
row_len = len(lines) 
col_len = len(lines[row])

for i in range(row_len):
    for j in range(col_len):
        if lines[i][j] == "NaN":
            lines[i][j] = 0

for i in range(1, row_len):
    for j in range(5, col_len):
        lines[i][j] =float(lines[i][j])

adj_index = lines[0].index("Adj Close")
month_index = lines[0].index("Month")
year_index = lines[0].index("Year")
return_index = lines[0].index("Return")
short_ma_index = lines[0].index("Short_MA")

#get lists of bid price and selling price
def getRecordOfTrades(lines):
    have_stock = False
    records = []
    for i in range(1, row_len):
        if have_stock == False:
            if lines[i][adj_index] > lines[i][short_ma_index]:
                bid_price = lines[i][adj_index]
                stock_bought = 100 // bid_price
                have_stock = True
            else: continue
        else:
            if lines[i][adj_index] <= lines[i][short_ma_index]:
                selling_price = lines[i][adj_index]
                revenue = selling_price * stock_bought
                profit = revenue - bid_price * stock_bought
                records.append(profit)
                have_stock = False
            else:
                continue
    return records

trade_records = getRecordOfTrades(lines)
trades_num = len(trade_records)
profitable_trades= 0
lossing_trades =0
total_profit = 0
total_loss = 0
for trade in trade_records:
    if trade > 0:
        profitable_trades += 1
        total_profit += trade
    elif trade < 0:
        lossing_trades += 1
        total_loss += trade
average_profit = total_profit / profitable_trades
average_profit = total_loss / lossing_trades
record_stat = [trades_num, profitable_trades, average_profit, lossing_trades, average_profit]


record_titles = ["Trades", "Profitable Trades", "Average Profit", "Lossing Trades", "Average Loss"]
results = {}
for k, v in zip(record_titles, record_stat):
    results[k] = v

print(results)