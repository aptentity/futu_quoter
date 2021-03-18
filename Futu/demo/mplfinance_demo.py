# -*- coding: utf-8 -*-

import mplfinance as mpf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime

# ---------从网络读取---------
# data = pdr.get_data_yahoo('SOXL', '2021/1/1', '2021/3/16')
# 写入csv
# data.to_csv('data.csv')

# ---------从文件读取---------
# 方法一
# dateparse = lambda dates: datetime.strptime(dates, '%Y-%m-%d')
# data = pd.read_csv('data.csv', index_col='Date', date_parser=dateparse)

# 方法二
data = pd.read_csv('data.csv', index_col='Date')
data.index = pd.DatetimeIndex(data.index)

print(data)
# mpf.plot(data)  # 美国线
# mpf.plot(data, type='line')  # 线性图
add_plot = mpf.make_addplot(data[['High', 'Low']])
# mpf.plot(data, type='candle', mav=(2, 5, 10), volume=True)  # 蜡烛图
# mpf.plot(data, type='candle', addplot=add_plot, volume=True)

print(mpf.available_styles())
# 在图上添加标记
a_list = data.High.tolist()
b_list = data.Low.tolist()
add_plot1 = [mpf.make_addplot(a_list, type='scatter', markersize=100, marker='v', color='y'),
             mpf.make_addplot(b_list, type='scatter', panel=0, markersize=100, marker='^', color='r'),
             mpf.make_addplot(data['Close'], panel=1, color='g', secondary_y='auto'),  # 副图
             ]
my_color = mpf.make_marketcolors(up='cyan', down='red', edge='black', wick='black', volume='blue')
my_style = mpf.make_mpf_style(marketcolors=my_color, gridaxis='both', gridstyle='-.', y_on_right=True)
mpf.plot(data, type='candle', addplot=add_plot1, volume=True, panel_ratios=(2.5, 1), style='blueskies', title='SOXL')

# macd
exp12 = data['Close'].ewm(span=12, adjust=False).mean()
exp26 = data['Close'].ewm(span=26, adjust=False).mean()
macd = exp12 - exp26
signal = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal
add_plot2 = [mpf.make_addplot(exp12, type='line', color='y'),
             mpf.make_addplot(exp26, type='line', color='r'),
             mpf.make_addplot(histogram, type='bar', width=0.7, panel=2, color='dimgray', alpha=1,
                              secondary_y=False),
             mpf.make_addplot(macd, panel=2, color='fuchsia', secondary_y=True),
             mpf.make_addplot(signal, panel=2, color='b', secondary_y=True),
             ]
mpf.plot(data, type='candle', addplot=add_plot2, volume=True, figscale=1.5, title='MACD', figratio=(5, 5),
         ylabel='price', ylabel_lower='volume',
         main_panel=0, volume_panel=1, )
