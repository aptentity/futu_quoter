# -*- coding: utf-8 -*-
from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
result = quote_ctx.get_market_snapshot('HK.00700')[1]
print(result['last_price'])
print(quote_ctx.get_market_snapshot('HK.00700'))  # 获取港股 HK.00700 的快照数据
quote_ctx.close() # 关闭对象，防止连接条数用尽