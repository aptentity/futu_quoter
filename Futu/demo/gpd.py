# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:13:00 2020

@author: howard

美国、中国、日本近二十年人均GDP对比图
"""

from pandas_datareader import wb
import matplotlib.pyplot as plt

dat = wb.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CN', 'JP'], start=2001, end=2021)
dat2draw = dat.unstack(level=0)

plt.figure(figsize=(10, 4))
plt.plot(dat2draw.iloc[:, 0], 'r-', label="China")
plt.plot(dat2draw.iloc[:, 1], 'b-*', label="Japan")
plt.plot(dat2draw.iloc[:, 2], 'g--', label="USA")
plt.title("PER CAPITA GDP ($)", fontsize=20)
plt.legend()
plt.pause(0)
