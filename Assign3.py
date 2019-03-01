#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 17:56:25 2019

@author: sinsakuokazaki
"""

#3.	 If your stock  is down W days in a row, buy on day W and sell next day: put $100 at adj closing price

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


#Get record of Trades 
def getRecordOfTrades(w):
    
    if w > 0:
        down_count = 0
        records = []
        for i in range(1, row_len):
            if w < row_len - i:
                if lines[i][return_index] < 0 :
                    down_count += 1
                else:
                    down_count = 0
                if down_count < w:
                    continue
                else:
                    bid_price =lines[i][adj_index]
                    stock_bought = 100 // bid_price
                    if stock_bought > 0:
                        selling_price = lines[i+1][adj_index]
                        revenue = selling_price * stock_bought
                        profit = revenue - bid_price * stock_bought
                        records.append(profit)
            else: break
    return records

ws = list(range(1,6))
record_titles = ["Trades", "Profitable Trades", "Average Profit", "Lossing Trades", "Average Loss"]
results = {}

for w in ws:
    trade_record = getRecordOfTrades(w)
    trades_num = len(trade_record)
    profitable_trades= 0
    lossing_trades =0
    total_profit = 0
    total_loss = 0
    for trade in trade_record:
        if trade > 0:
            profitable_trades += 1
            total_profit += trade
        elif trade < 0:
            lossing_trades += 1
            total_loss += trade
    average_profit = total_profit / profitable_trades
    average_loss = total_loss / lossing_trades
    record_stat = [trades_num, profitable_trades, average_profit, lossing_trades, average_profit]
    
    result= {}
    for k, v in zip(record_titles, record_stat):
        result[k] = v
    results[w] = result
    
for k in results.keys():
    print(k,"| ", results[k])
    
