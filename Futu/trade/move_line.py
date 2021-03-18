# -*- coding: utf-8 -*-

import mplfinance
import tushare as ts
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.pylab import date2num
import numpy as np
import matplotlib as mpl
ts.set_token('a7e1128b97276a0996efd8cd26b82b601638533646a3c0a39ddb96f8')
sns.set()
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'SimHei'
pro = ts.pro_api()

df = pro.index_daily(ts_code='000001.SH', start_date='20170101')
df = df.sort_values(by='trade_date', ascending=True)
df['trade_date2'] = df['trade_date'].copy()
df['trade_date'] = pd.to_datetime(df['trade_date']).map(date2num)
df['dates'] = np.arange(0, len(df))
df.head()
print(df)