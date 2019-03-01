#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:43:03 2019

@author: sinsakuokazaki
"""

#1.	If you decide to hold a stock for 1 day, what is the best day of the week to do so –
#For each day of the week, compute average, min and max of daily returns


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
    
#Get list of Return values
return_index = lines[0].index("Return")
weekday_index = lines[0].index("Weekday")
#Get lists of Return values for each day of the week
mon = []
tue = []
wed = []
thu = []
fri = []
for i in range(1, row_len):
    if lines[i][weekday_index] == "Monday":
        mon.append(lines[i][return_index])
        
    elif lines[i][weekday_index] == "Tuesday":
        tue.append(lines[i][return_index])
        
    elif lines[i][weekday_index] == "Wednesday":
        wed.append(lines[i][return_index])
        
    elif lines[i][weekday_index] == "Thursday":
        thu.append(lines[i][return_index])
        
    else: 
        fri.append(lines[i][return_index])


return_weekday = [mon, tue, wed, thu, fri]
stat_key = ["min", "max", "average", "median"]


#function to get a list of statistics 
def getStatistics(nums):
    values = []
    values.append(min(nums))
    values.append(max(nums))
    values.append(mean(nums))
    values.append(median(nums))
    return values

#Store results into dictionary
result_mon = {}
result_tue = {}
result_wed = {}
result_thu = {}
result_fri = {}
for i in range(len(return_weekday)):
    stat_value = getStatistics(return_weekday[i])
    for k, v in zip(stat_key, stat_value):
        if i == 0:
            result_mon[k] = v
        elif i == 1:
            result_tue[k] = v
        elif i == 2:
            result_wed[k] = v
        elif i ==3:
            result_thu[k] = v
        else:
            result_fri[k] = v
            


print("Monday|  ", result_mon, end = '\n\n')
print("Tuesday|  ", result_tue, end = '\n\n')
print("Wedneday|  ", result_wed, end = '\n\n')
print("Thursday|  ", result_thu, end = '\n\n')
print("Friday|  ", result_fri, end = '\n\n')







    
    
    