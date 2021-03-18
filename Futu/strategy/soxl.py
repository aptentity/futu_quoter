# -*- coding: utf-8 -*-
# SOXL的策略
from futu import *
import mplfinance as mpf
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime

pd.set_option('display.max_columns', 1000)  # 设置最大显示列数的多少
pd.set_option('display.width', 10000)  # 设置宽度,就是说不换行,比较好看数据
pd.set_option('display.max_rows', 500)  # 设置行数的多少


# ----------1 读取K线数据------------
def read_k_data(stock, download):
    if download == 1:
        quote_ctx.subscribe([stock_code], [period])
        k_ret, k_data = quote_ctx.get_cur_kline(stock_code, 200, period, AuType.QFQ)
        if k_ret != RET_OK:
            return k_ret, k_data
        else:
            k_data.rename(
                columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'time_key': 'Date',
                         'volume': 'Volume'},
                inplace=True)  # 列重命名
            k_data = k_data.set_index(['Date'])  # 更改index
            k_data.index = pd.DatetimeIndex(k_data.index)  # 更改index的类型
            k_data.to_csv('data.csv')
    else:
        k_data = pd.read_csv('data.csv', index_col='Date')
        k_data.index = pd.DatetimeIndex(k_data.index)
    return RET_OK, k_data


# --------------计算均线--------------
def get_line_data(k_data):
    m_step = 20
    b_step1 = 30
    b_step2 = 72
    gap = 0.05

    t_m_line = k_data['Close'].ewm(span=m_step, adjust=False).mean()  # m线
    t_b_line1 = k_data['Close'].ewm(span=b_step1, adjust=False).mean()
    t_b_line2 = k_data['Close'].ewm(span=b_step2, adjust=False).mean()
    t_b_line = (t_b_line1 + t_b_line2) / 2
    t_t1 = t_m_line * (1 + 2 * gap)
    t_t2 = t_m_line * (1 + gap)
    t_b1 = t_m_line * (1 - 2 * gap)
    t_b2 = t_m_line * (1 - gap)
    return t_m_line, t_b_line, t_t1, t_t2, t_b1, t_b2


# -------------计算突破------------------
def get_signal(k_data, t_t1, t_b1):
    t_high = []
    t_low = []
    t_line_size = len(k_data)
    for n in range(t_line_size):
        if k_data['High'][n] < t_t1[n]:
            t_high.append(np.nan)
        else:
            t_high.append(k_data['High'][n])
        if k_data['Low'][n] > t_b1[n]:
            t_low.append(np.nan)
        else:
            t_low.append(k_data['Low'][n])
    return t_high, t_low


download_data = 0  # 是否重新读取数据
stock_code = 'HK.07226'  # 股票代码 US.SOXL
period = SubType.K_30M  # 周期

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
print('-------------------------')
ret, data = read_k_data(stock_code, download_data)
m_line, b_line, t1, t2, b1, b2 = get_line_data(data)
high, low = get_signal(data, t1, b1)

# macd
exp12 = data['Close'].ewm(span=12, adjust=False).mean()
exp26 = data['Close'].ewm(span=26, adjust=False).mean()
macd = exp12 - exp26
signal = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal
add_plot2 = [mpf.make_addplot(m_line, type='line', color='y'),
             mpf.make_addplot(b_line, type='line', color='r'),
             mpf.make_addplot(t1, type='line', color='b'),
             mpf.make_addplot(t2, type='line', color='b'),
             mpf.make_addplot(b1, type='line', color='g'),
             mpf.make_addplot(b2, type='line', color='g'),
             mpf.make_addplot(high, type='scatter', markersize=10, marker='v', color='y'),
             mpf.make_addplot(low, type='scatter', markersize=10, marker='^', color='r'),
             mpf.make_addplot(histogram, type='bar', width=0.7, panel=1, color='dimgray', alpha=1,
                              secondary_y=False),
             mpf.make_addplot(macd, panel=1, color='fuchsia', secondary_y=True),
             mpf.make_addplot(signal, panel=1, color='b', secondary_y=True),
             ]

mpf.plot(data, type='candle', addplot=add_plot2, volume=False, figscale=1.5, title='MACD', figratio=(5, 5),
         ylabel='price', ylabel_lower='volume',
         main_panel=0, volume_panel=1, )

exit()


#
class CurKlineCHandler(CurKlineHandlerBase):
    def on_recv_rsp(self, content):
        ret_code, data_k = super(CurKlineCHandler, self).on_recv_rsp(content)
        if ret_code != RET_OK:
            print("CurKline: error, msg: %s" % data_k)
            return RET_ERROR, data_k
        print("CurKline ", data_k)  # StockQuoteTest自己的处理逻辑
        return RET_OK, data_k


quote_handler = CurKlineCHandler()
# quote_ctx.set_handler(quote_handler)

ret_sub, err_message = quote_ctx.subscribe([stock_code], [period])
# 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline(stock_code, 200, period, AuType.QFQ)  # 获取港股00700最近2个K线数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)

# time.sleep(100000)

# ---------------2 数据调整----------
data.rename(
    columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'time_key': 'Date', 'volume': 'Volume'},
    inplace=True)  # 列重命名
data = data.set_index(['Date'])  # 更改index
data.index = pd.DatetimeIndex(data.index)  # 更改index的类型

# --------------3 计算均线------------


# --------------4 计算突破-----------------
