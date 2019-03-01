#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:14:07 2019

@author: sinsakuokazaki
"""


import numpy as np 
import pandas as pd

df = pd.read_csv("ORCL.csv")
mean = df["Return"].mean()
sd = df["Return"].std()
return_list = df["Return"]

count_tail = 0
count_head = 0
for i in range(len(return_list)):
    if return_list[i] < mean - 2*sd:
        count_tail += 1
    elif return_list[i] > mean + 2*sd:
        count_head += 1
    
days_result = count_tail + count_head
days_5percent = len(return_list) * 5 / 100

print("The days outside mean +/- 2 * st_dev is", days_result)
print("5% predicted by normal distribution is", days_5percent)
print("\nThe days out side mean +/- 2 * st_dev is slightly less than 5 % predicted by normal distribution")