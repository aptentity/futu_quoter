# -*- coding: utf-8 -*-
from collections import namedtuple
from collections import OrderedDict
from functools import reduce
import my_function
import stock_trade_days

price_str = '30,20,40,50,10,60'
print(type(price_str))

if not isinstance(price_str, str):
    price_str = str(price_str)
    print(type(price_str))
    print(price_str)

print('旧的price_str={} id={}'.format(price_str, id(price_str)))
price_str = price_str + ',70'
# price_str = price_str.replace('1', '2')
print('新的price_str={} id={}'.format(price_str, id(price_str)))

price_array = price_str.split(',')
print(price_array)
price_array.append('15')
print(price_array)
print(len(price_array))
price_set = set(price_array)
print(price_set)
print(len(price_set))

for price in price_set:
    print(price)

# 列表推导式
date_base = 20170118
date_array = [str(date_base + ind) for ind, _ in enumerate(price_array)]
print(date_array)

# zip
stock_tuple_list = [(date, price) for date, price in zip(price_array, date_array)]
print(stock_tuple_list)
print(stock_tuple_list[0])
print(stock_tuple_list[0][0])

# 可命名元组
stock_namedtuple = namedtuple('stock', ('date', 'price'))
stock_namedtuple_list = [stock_namedtuple(date, price) for date, price in zip(date_array, price_array)]
print(stock_namedtuple_list)
for stock in stock_namedtuple_list:
    print(stock.date + ',' + stock.price)

# 字典推导式
stock_dict = {date: price for date, price in zip(date_array, price_array)}
print(stock_dict)
print(stock_dict.keys())
print(stock_dict.values())
# 遍历字典
# 方法一：遍历key值
for date in stock_dict:
    print(date + ',' + stock_dict[date])

# 方法二：遍历字典项
for stock in stock_dict.items():
    print(stock)

# 方法三：遍历字典键值
for date, price in stock_dict.items():
    print(date + ',' + price)

# 有序字典
stock_ordered_dict = OrderedDict((date, price) for date, price in zip(date_array, price_array))
print(stock_ordered_dict.keys())

print(min(stock_dict))  # 最小日期
print(min(stock_dict.values()))  # 最小收盘价
print(min(zip(stock_dict.values(), stock_dict.keys())))  # 最小收盘价和对应的日期
print(min(zip(stock_dict.keys(), stock_dict.values())))  # 最小日期和对应的收盘价

print(my_function.find_second_max(stock_dict))
print(my_function.find_second_max_lambda(stock_dict))

print('---高阶函数---')
# float类型的价格列表
price_float_array = [float(price_str) for price_str in stock_dict.values()]
print('price_float_array=')
print(price_float_array)
# 时间平移
# [:-1]:从第0个到倒数第二个
# [1:]：从第一个到最后一个
pp_array = [(price1, price2) for price1, price2 in zip(price_float_array[:-1], price_float_array[1:])]
print(pp_array)

print(reduce(lambda x, y: x + y, (1, 2, 3, 4, 5, 6, 7)))
# print(list(map(lambda x: x ** 2, [1, 2, 3, 4, 5])))

change_array = list(map(lambda pp: reduce(lambda a, b: round((b - a) / a, 3), pp), pp_array))
change_array.insert(0, 0)
print(change_array)

print(date_array)
print(price_array)
print(change_array)
stock_namedtuple = namedtuple('stock', ('date', 'price', 'change'))
stock_dict = OrderedDict(
    (date, stock_namedtuple(date, price, change)) for date, price, change in zip(date_array, price_array, change_array))
print(stock_dict)

print('所有上涨的交易日：{}'.format(list(my_function.filter_stock(stock_dict))))
print('所有下跌的交易日：{}'.format(list(my_function.filter_stock(stock_dict, want_up=False))))
print('所有上涨交易日的涨幅和：{}'.format(my_function.filter_stock(stock_dict, want_calc_sum=True)))
print('所有下跌交易日的跌幅和：{}'.format(my_function.filter_stock(stock_dict, want_up=False, want_calc_sum=True)))

print('所有上涨的交易日：{}'.format(list(my_function.filter_stock_up_days(stock_dict))))
print('所有下跌的交易日：{}'.format(list(my_function.filter_stock_down_days(stock_dict))))
print('所有上涨交易日的涨幅和：{}'.format(my_function.filter_stock_up_sums(stock_dict)))
print('所有下跌交易日的跌幅和：{}'.format(my_function.filter_stock_down_sums(stock_dict)))

print('----------------函数-----------------')
price_array = '30.14,29.58,26.36,32.56,32.82'.split(',')
date_base = 20170118
trade_days = stock_trade_days.StockTradeDays(price_array, date_base)
print(trade_days)
print('trade_days对象长度为{}'.format(len(trade_days)))
print(list(trade_days.filter_stock()))
print(list(trade_days.filter_stock(want_up=False)))
print(trade_days.filter_stock(want_calc_sum=True))
print(trade_days.filter_stock(want_up=False, want_calc_sum=True))
