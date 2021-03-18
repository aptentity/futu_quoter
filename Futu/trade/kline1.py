# -*- coding: utf-8 -*-

import pyecharts.options as opts
from pyecharts.charts import Candlestick

x_data = ["2017-10-24", "2017-10-25", "2017-10-26", "2017-10-27"]
y_data = [[20, 30, 10, 35], [40, 35, 30, 55], [33, 38, 33, 40], [40, 40, 32, 42]]
(Candlestick(init_opts=opts.InitOpts(width='1200px', height='600px'))
 .add_xaxis(xaxis_data=x_data)
 .add_yaxis(series_name='', y_axis=y_data)
 .set_series_opts()
 .set_global_opts(yaxis_opts=opts.AxisOpts(
    splitarea_opts=opts.SplitLineOpts(
        is_show=True, linestyle_opts=opts.LineStyleOpts(width=1)
    )
)).render('kline1.html'))
