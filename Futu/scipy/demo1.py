# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import statsmodels.api as sm

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
data = pd.read_csv('data.csv', index_col='Date')
data.index = [dt.datetime.strptime(x, '%Y-%m-%d') for x in data.index]
print(data.head())
#data.plot(figsize=(10, 6))
#plt.ylabel('涨跌幅')

x = data['沪深300'].values
y = data['中国平安'].values
X = sm.add_constant(x)  # 添加常数项
model = sm.OLS(y, X)  # 最小二乘法
results = model.fit()
print(results.params)

plt.plot(x, y, 'o', label='中国平安-沪深300')
plt.plot(x, results.fittedvalues, 'r--', label='OLS')
plt.legend()
plt.xlabel('沪深300')
plt.ylabel('中国平安')
plt.grid(True)

plt.pause(0)
