#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:22:18 2019

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

drink = ['Hot chocolate', 'Coffee','Tea', 'Mineral water', 'Juice', 'Smoothies', 'Coke']
food = ['Bread', 'Scandinavian', 'Jam', 'Cookies','Muffin', 'Pastry','Medialuna', 'Tartine', 'Frittata', 'Hearty & Seasonal', 'Soup', 'Chicken sand','Cake','Focaccia','Sandwich', 'Alfajores', 'Eggs', 'Brownie', 'Dulce de Leche', 'Honey', 'Granola', 'Empanadas', 'Bread Pudding', 'Truffles', 'Bacon', 'Spread', 'Kids biscuit', 'Caramel bites', 'Jammie Dodgers', 'Polenta', 'Bakewell', 'Lemon and coconut', 'Toast', 'Scone', 'Crepes', 'Vegan mincepie', 'Bare Popcorn', 'Muesli', 'Crisps', 'Pintxos', 'Gingerbread syrup', 'Panatone', 'Brioche and salami', 'Salad', 'Chicken Stew', 'Spanish Brunch', 'Raspberry shortbread sandwich', 'Extra Salami or Feta', 'Duck egg', 'Baguette', 'Chocolates', 'Cherry me Dried fruit', 'Tacos/Fajita']
unknown = ['NONE', 'Basket', 'Farm House', 'Fudge', "Ella's Kitchen Pouches", 'Victorian Sponge', 'Pick and Mix Bowls', 'Mighty Protein', 'My-5 Fruit Shoot', 'The BART', 'Fairy Doors', 'Keeping It Local', 'Art Tray', 'Bowl Nic Pitt', 'Adjustment', 'Chimichurri Oil', 'Siblings', 'Tiffin', 'Olum & polenta', 'The Nomad', 'Hack the stack', 'Afternoon with the baker', "Valentine's card", 'Tshirt', 'Vegan Feast', 'Postcard', 'Nomad bag', 'Coffee granules ', 'Drinking chocolate spoons ', 'Christmas common', 'Argentina Night', 'Half slice Monster ', 'Gift voucher', 'Mortimer', 'Raw bars']

#create item category column
def createCategory(items):
    item_category = []
    for item in items:
        if item in food:
            item_category.append("food")
        elif item in unknown:
            item_category.append("unknown")
        elif item in drink:
            item_category.append("drink")
    return item_category

df["Item_Category"]  = createCategory(df['Item'])


#get price for each food item
food_price = df.loc[df['Item_Category'] == 'food'].groupby(['Item'])['Item_Price'].mean()
#get average of all kinds of food items
ave_food_price = food_price.mean()

print("The average of all kinds of food is", ave_food_price)

#get total sales for both drinks and foods
sales_for_category = df['Item_Price'].groupby(df['Item_Category']).sum()
drink_sales = sales_for_category['drink']
food_sales = sales_for_category['food']

print("The sales of drinks is", drink_sales)
print("The sales of foods is", food_sales)
print("The sales of foods is higer than drinks, but both make quite money.")

#function to create dictionary showing top 5 popular items for each given times 
def createTop5Dict(time):
    items_for_time = df.groupby(time)['Item'].value_counts()
    times = np.sort(df[time].unique())
    popularity = {}
    for t in times:
        if len(items_for_time[t]) >= 5:
            popularity[t] = items_for_time[t][:5]
        else:
            popularity[t] = items_for_time[t][:]
    return popularity

#function to create dictionary showing bottom 5 popular items for each given times 
def createBottom5Dict(time):
    items_for_time = df.groupby(time)['Item'].value_counts()
    times = np.sort(df[time].unique())
    popularity = {}
    for t in times:
        if len(items_for_time[t]) >= 5:
            popularity[t] = items_for_time[t][-1:-6:-1]
        else:
            popularity[t] = items_for_time[t][-1::-1]
    return popularity

top_hour = createTop5Dict('Hour')
bottom_hour = createBottom5Dict('Hour')
top_weekday = createTop5Dict('Weekday')
bottom_weekday = createBottom5Dict('Weekday')
top_period = createTop5Dict('Period')
bottom_period = createBottom5Dict('Period')


for t, d in zip(["hour", "weekday", "period"], [top_hour, top_weekday, top_period]):
    print("")
    print("Top 5 popular items for {0}. When the total unique items bought in the {0} are less than 5, show all the items ".format(t))
    
    for k in d.keys():
        print("{0}:".format(k))
        for i in range(len(d[k])):
            print(d[k].index[i], end = " ,")
        print("")
        
for t, d in zip(["hour", "weekday", "period"], [bottom_hour, bottom_weekday, bottom_period]):
    print("")
    print("Bottom 5 popular items for {0}. When the total unique items bought in the {0} are less than 5, show all the items ".format(t))
    
    for k in d.keys():
        print("{0}:".format(k))
        for i in range(len(d[k])):
            print(d[k].index[i], end = " ,")
        print("")


#Calculate how many drinks are ordered per transaction
drinks_per_trans = df.loc[df['Item_Category'] == 'drink'].groupby('Transaction')['Item_Category'].count()
#Calculate frequency of each groupsize
frequency_groupsize = drinks_per_trans.value_counts()

#create a dictionary containing probability of group size
total_transactions = frequency_groupsize.sum()
groupsize_percentage = {}
for i in frequency_groupsize.index :
    groupsize_percentage[i] = frequency_groupsize[i] / total_transactions * 100
    
print("")
for k, v in groupsize_percentage.items():
    print("The probability of being group size {0} is {1}%".format(k, v))
    
    
    
    