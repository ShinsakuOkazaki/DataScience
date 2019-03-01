#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:22:16 2019

@author: sinsakuokazaki
"""


import numpy as np 
import pandas as pd


df = pd.read_csv("ORCL_digit_analysis.csv")
freq = df["digit_frequency"]
pred = df["uniform"]

def absErr(freq, pred):
    abs_err = []
    for f, p in zip(freq, pred):
        abs_err.append(abs(f - p))
    return abs_err

def sqErr(freq, pred):
    sq_err = []
    for f, p in zip(freq, pred):
        sq_err.append((f - p)**2)
    return sq_err

abs_err = absErr(freq, pred)
sq_err = sqErr(freq, pred)

max_abs_err = max(abs_err)
med_abs_err = np.median(abs_err)
mae = np.mean(abs_err)
rmse = np.sqrt(np.mean(sq_err))

print("Max Absolute Error is", max_abs_err)
print("Meidan Absolute Error is", med_abs_err)
print("MAE is", mae)
print("RMSE is", rmse)