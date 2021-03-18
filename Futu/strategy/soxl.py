# -*- coding: utf-8 -*-
# SOXL的策略
from futu import *
import mplfinance as mpf
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime

pd.set_option('display.max_columns', 1000)  # 设置最大显示列数的多少
pd.set_option('display.width', 10000)  # 设置宽度,就是说不换行,比较好看数据
pd.set_option('display.max_rows', 500)  # 设置行数的多少

download_data = 0  # 是否重新读取数据
stock_code = 'HK.07226'  # 股票代码
period = SubType.K_3M  # 周期

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
print('-------------------------')


# ----------1 读取K线数据------------

class CurKline(CurKlineHandlerBase):
    def on_recv_log(self, content):
        ret_code, data_k = super(CurKline, self).on_recv_rsp(content)
        if ret_code != RET_OK:
            print("CurKline: error, msg: %s" % data_k)
            return RET_ERROR, data_k
        print("CurKline ", data_k)  # StockQuoteTest自己的处理逻辑
        return RET_OK, data_k


# quote_handler = CurKline()
# quote_ctx.set_handler(quote_handler)
ret_sub, err_message = quote_ctx.subscribe(stock_code, [period])
# 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline(stock_code, 200, period, AuType.QFQ)  # 获取港股00700最近2个K线数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)

# ---------------2 数据调整----------
data.rename(
    columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'time_key': 'Date', 'volume': 'Volume'},
    inplace=True)  # 列重命名
data = data.set_index(['Date'])  # 更改index
data.index = pd.DatetimeIndex(data.index)  # 更改index的类型

# macd
exp12 = data['Close'].ewm(span=12, adjust=False).mean()
exp26 = data['Close'].ewm(span=26, adjust=False).mean()
macd = exp12 - exp26
signal = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal
add_plot2 = [mpf.make_addplot(exp12, type='line', color='y'),
             mpf.make_addplot(exp26, type='line', color='r'),
             mpf.make_addplot(histogram, type='bar', width=0.7, panel=1, color='dimgray', alpha=1,
                              secondary_y=False),
             mpf.make_addplot(macd, panel=1, color='fuchsia', secondary_y=True),
             mpf.make_addplot(signal, panel=1, color='b', secondary_y=True),
             ]

mpf.plot(data, type='candle', addplot=add_plot2, volume=False, figscale=1.5, title='MACD', figratio=(5, 5),
         ylabel='price', ylabel_lower='volume',
         main_panel=0, volume_panel=1, )


