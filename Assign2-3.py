#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:25:23 2019

@author: sinsakuokazaki
"""

import math
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations 

df = pd.read_csv("BreadBasket_DMS_output.csv")
#function for craete period column
def createPeriod(hours):
    periods = []
    for hour in hours:
        if hour >= 0 and hour < 6:
            periods.append("night")
        elif hour >=6 and hour < 12:
            periods.append("morning")
        elif hour >= 12 and hour < 18:
            periods.append("afternoon")
        elif hour >= 18 and hour <= 23:
            periods.append("evening")
        else: periods.append("Nan")
    return periods
df["Period"] = createPeriod(df["Hour"])

#get busiest hour, weekday and period
trans_for_hour = df.groupby('Hour')['Transaction'].nunique()
busiest_hour = trans_for_hour.idxmax()

trans_for_weekday = df.groupby('Weekday')['Transaction'].nunique()
busiest_weekday = trans_for_weekday.idxmax()

trans_for_period = df.groupby('Period')['Transaction'].nunique()
busiest_period = trans_for_period.idxmax()

print("The busiest hour is", busiest_hour)
print("The busiest weekday is", busiest_weekday)
print("The busiest period is", busiest_period)

#function to get most profitable time
def profitOfHours(times, column):
    profits = {}
    for time in times: 
        profits[time] = df.loc[df[column] == time]["Item_Price"].sum()
    return profits

def getMostProfitable(column):
    times = df[column].unique()
    profits = profitOfHours(times, column)
    max_profit = max(profits.values())
    most_profitable_times = []
    for k, v in profits.items():
        if profits[k] == max_profit:
            most_profitable_times.append(k)
    return most_profitable_times
#get most profitable hour, weekday, period
most_profitable_hour = getMostProfitable("Hour")
most_profitable_weekday = getMostProfitable("Weekday")
most_profitable_period = getMostProfitable("Period")

print("The most profitable hour is", most_profitable_hour)
print("The most profitable weekday is", most_profitable_weekday)
print("The most profitable period is", most_profitable_period)

#functions to get most and least frequent value in column
def getFrequencyFromSorted(counts):
    frequent_values = []
    for count, value in zip(counts, counts.index):
        if count == counts.iloc[0]:
            frequent_values.append(value)
        else:
            break
    return frequent_values

def getMostFrequentValues(column):
    counts_descend = df[column].value_counts()
    return getFrequencyFromSorted(counts_descend)
    
def getLeastFrequentValues(column):
    counts_ascending = df[column].value_counts(ascending = True)
    return getFrequencyFromSorted(counts_ascending)
#get most and least popular items
most_popular_item = getMostFrequentValues("Item")
least_popular_item = getLeastFrequentValues("Item")

print("The most popular item is", most_popular_item)
print("The least popular items are", least_popular_item)


#function to delete NONE value
def deleteNone(items):
    for i in items.index:
        if "NONE" in items[i]:
            index = np.argwhere(items[i] == "NONE")
            items[i] = np.delete(items[i], index)
        if len(items[i]) < 2:
            items = items.drop(i)
    return items
#function to create list of combinations
def generateCombinations(item_choices):
    none_index = np.argwhere(item_choices == "NONE")
    item_choices = np.delete(item_choices, none_index)
    combs = []
    for comb in combinations(item_choices, 2):
        combs.append(comb)
    return combs

#function to create dictionary to count the frequency of the combination
def generateCombsDict(combs, items):
    combs_dict ={}
    for k in combs:
        combs_dict[k] = 0
    for comb in combs:
        for item in items:
            if set(comb).issubset(item):
                combs_dict[comb] += 1
    return combs_dict

#function to calculate the most and the least popular combinations
def getMostAndLeastPopulor(combs_dict):
    max_value = max(combs_dict.values())
    min_value = min(combs_dict.values())
    max_combs = []
    min_combs = []
    for k, v in combs_dict.items():
        if v == max_value:
            max_combs.append(k)
        if v == min_value:
            min_combs.append(k)
    return max_combs, min_combs

#get items per each transaction
items = df.groupby('Transaction')['Item'].unique()
items = deleteNone(items)
item_choices = df['Item'].unique()
combs = generateCombinations(item_choices)
combs_dict = generateCombsDict(combs, items)
most_combs, least_combs = getMostAndLeastPopulor(combs_dict)

print("The most frequent combination is", most_combs)
print("There are too many combinations that never appear in the data, so I decided not to print out. Check value of 'least_combs'")

#get number of transactions per day
trans_per_day = df.groupby(['Year', 'Month', 'Day', 'Weekday'])['Transaction'].count()
#convert multiple index to dataframe
df_trans_per_day = trans_per_day.to_frame()
#get average number of transactions for day of the week
ave_trans_for_weekday = df_trans_per_day.groupby('Weekday')['Transaction'].mean()

#get dictionary that contains how many baristas we need for day of the week
weekdays = df['Weekday'].unique()
barista_dict = {}
for weekday in weekdays:
    barista_dict[weekday] = int(round(ave_trans_for_weekday[weekday] / 60.0))

for k, v in barista_dict.items():
    print("On {0}, {1} baristas are needed". format(k, v))