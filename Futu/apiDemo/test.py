# -*- coding: utf-8 -*-
from futu import *
import pandas as pd

pd.set_option('display.max_columns', 1000)   # 设置最大显示列数的多少
pd.set_option('display.width', 10000)         # 设置宽度,就是说不换行,比较好看数据
pd.set_option('display.max_rows', 500)       # 设置行数的多少

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
print('-------------------------')
print('获取全局市场状态')
print(quote_ctx.get_global_state())  # 获取全局市场状态

print('-------------------------')
print('获取港股')
print(quote_ctx.get_market_snapshot('HK.00700'))  # 获取港股 HK.00700 的快照数据

print('-------------------------')
print('实时报价')


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_log(self, content):
        ret_code, data = super(StockQuoteTest,self).on_recv_rsp(content)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data
        print("StockQuoteTest ", data)  # StockQuoteTest自己的处理逻辑
        return RET_OK, data


quote_handler = StockQuoteTest()
quote_ctx.set_handler(quote_handler)
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.QUOTE])

# 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_stock_quote(['HK.00700'])  # 获取订阅股票报价的实时数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)

print('-------------------------')
print('实时摆盘')


class OrderBookTest(OrderBookHandlerBase):
    def on_recv_log(self, content):
        ret_code,data = super(OrderBookTest,self).on_recv_rsp(content)
        if ret_code != RET_OK:
            print("OrderBookTest: error, msg: %s" % data)
            return RET_ERROR, data
        print("OrderBookTest ", data) # OrderBookTest自己的处理逻辑
        return RET_OK, data


order_handler = OrderBookTest
quote_ctx.set_handler(order_handler)
ret_sub = quote_ctx.subscribe(['HK.00700'], [SubType.ORDER_BOOK])[0]
# 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    # ret, data = quote_ctx.get_stock_quote(['HK.00700'])  # 获取订阅股票报价的实时数据
    ret, data = quote_ctx.get_order_book('HK.00700')
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)


print('-------------------------')
print('实时K线')
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.K_DAY])
# 先订阅K 线类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_cur_kline('HK.00700', 10, SubType.K_DAY, AuType.QFQ)  # 获取港股00700最近2个K线数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)


print('-------------------------')
print('实时分时')
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.RT_DATA])
# 先订阅分时数据类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:   # 订阅成功
    ret, data = quote_ctx.get_rt_data('HK.00700')   # 获取一次分时数据
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)


print('-------------------------')
print('实时逐笔')
ret_sub, err_message = quote_ctx.subscribe(['HK.00700'], [SubType.TICKER])
# 先订阅逐笔类型。订阅成功后FutuOpenD将持续收到服务器的推送，False代表暂时不需要推送给脚本
if ret_sub == RET_OK:  # 订阅成功
    ret, data = quote_ctx.get_rt_ticker('HK.00700', 20)  # 获取港股00700最近2个逐笔
    if ret == RET_OK:
        print(data)
    else:
        print('error:', data)
else:
    print('subscription failed', err_message)


print('-------------------------')
print('自选股列表')
ret, data = quote_ctx.get_user_security('沪深')
if ret == RET_OK:
    print(data)
else:
    print('error:', data)

print('-------------------------')
print('自选股分组')
ret, data = quote_ctx.get_user_security_group(group_type=UserSecurityGroupType.ALL)
if ret == RET_OK:
    print(data)
else:
    print('error:', data)

# time.sleep(15)
quote_ctx.close()  # 关闭对象，防止连接条数用尽
