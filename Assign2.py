#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:31:03 2019

@author: sinsakuokazaki
"""

#2.	If you decide to buy a stock for one month, what would be the best/worst month?


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


#function to calculate average of daily returns
def mean(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)

#function to calculate median of daily returns
def median(numbers):
    numbers.sort()
    numbers_len = len(numbers)
    if not numbers:
        return None
    if numbers_len % 2 == 0:
        return (numbers[(numbers_len//2)] + numbers[(numbers_len//2) - 1]) / 2.0
    else:
        return numbers[(numbers_len-1)//2]
    

adj_index = lines[0].index("Adj Close")
month_index = lines[0].index("Month")
year_index = lines[0].index("Year")
#calculate returns for a month
def returnOfMonth(year, month):
    adjs_in_month = []
    for i in range(1, row_len):
        if lines[i][year_index] == year and lines[i][month_index] == month:
            adjs_in_month.append(lines[i][adj_index])
    first_adj = adjs_in_month[0]
    last_adj = adjs_in_month.pop()
    return last_adj - first_adj
            
#search first day and lastday of month
years_list = ["2014", "2015", "2016", "2017", "2018"]
months_list = [str(n) for n in range(1, 13)]

def returnsDict(years, months):
    returns_dict = {}
    for year in years:
        for month in months_list:
            ret = returnOfMonth(year, month)
            month_in_year = (year, month)
            returns_dict[month_in_year] = ret
    return returns_dict

returns_dict = returnsDict(years_list, months_list)

#Get statistics
def getStatistics(nums):
    values = []
    values.append(min(nums))
    values.append(max(nums))
    values.append(mean(nums))
    values.append(median(nums))
    return values


stat_keys = ["min", "max", "average", "median"]
return_in_month = {}
for month in months_list:
    returns_list = []
    for k, v in returns_dict.items():
        if k[1] == month:
            returns_list.append(v)
    stat_values = getStatistics(returns_list)
    stat_dict = {}
    for k, v in zip(stat_keys, stat_values):
        stat_dict[k] = v
    return_in_month[month] = stat_dict

months_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "Nobember", "December"]

for k, m in zip(return_in_month.keys(), months_name):
        print(m, "| ", return_in_month[k])









