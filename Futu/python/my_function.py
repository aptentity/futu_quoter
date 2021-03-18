# -*- coding: utf-8 -*-
from collections import OrderedDict
from functools import partial


# 找一个序列中第二大值
def find_second_max(dict_array):
    stock_prices_sorted = sorted(zip(dict_array.values(), dict_array.keys()))
    return stock_prices_sorted[-2]


find_second_max_lambda = lambda dict_array: sorted(zip(dict_array.values(), dict_array.keys()))[-2]


def filter_stock(stock_array_dict, want_up=True, want_calc_sum=False):
    if not isinstance(stock_array_dict, OrderedDict):
        raise TypeError('stock_array_dict must be OrderedDict!')
    filter_func = (lambda day: day.change > 0) if want_up else (lambda day: day.change < 0)
    want_days = filter(filter_func, stock_array_dict.values())
    if not want_calc_sum:
        return want_days
    change_sum = 0.0
    for day in want_days:
        change_sum += day.change
    return change_sum


filter_stock_up_days = partial(filter_stock, want_up=True, want_calc_sum=False)
filter_stock_down_days = partial(filter_stock, want_up=False, want_calc_sum=False)
filter_stock_up_sums = partial(filter_stock, want_up=True, want_calc_sum=True)
filter_stock_down_sums = partial(filter_stock, want_up=False, want_calc_sum=True)
