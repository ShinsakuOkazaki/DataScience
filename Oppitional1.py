#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 10:50:08 2019

@author: sinsakuokazaki
"""

#Optional Assignments:
#Assume you know tomorrow, start with a $100
#Q: how much money would you have on 12/31/2018?


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

#if do not have stock and Adj close of tomorrow is higher than today, buy the stock
#if do not have stock and Adj close of tomorrow is same or lower than today, wait for tomorrow 
#if have stock and Adj close of tomorrow is lower than today, sell the stock
#if have stock and Adj close of tomorrow is same or higher than today, wait for tomorrow
def getRecordOfTrades(lines):
    have_stock = False
    records = []
    for i in range(1, row_len):
        if i < row_len - 1:
            if have_stock == False:
                if lines[i][adj_index] < lines[i+1][adj_index]:
                    bid_price = lines[i][adj_index]
                    stock_bought = 100 * bid_price
                    have_stock = True
                else:
                    continue
            else:
                if lines[i][adj_index] > lines[i+1][adj_index]:
                    selling_price = lines[i][adj_index]
                    revenue = selling_price * stock_bought
                    profit = revenue - bid_price * stock_bought
                    records.append(profit)
                    have_stock = False
                else:
                    continue
        else:
            if not have_stock:
                break
            else:
                selling_price = lines[i][adj_index]
                revenue = selling_price * stock_bought
                profit = revenue - bid_price * stock_bought
                records.append(profit)
                have_stock = False
    return records



trade_records = getRecordOfTrades(lines)
total = sum(trade_records)
print("I have $", total, )
