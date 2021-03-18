# -*- coding: utf-8 -*-

import pandas as pd

amount = pd.Series([100, 90, 110, 150, 110, 130, 80, 90, 100, 150])
print('rolling sum')
print(amount.rolling(3).sum())
print('rolling sum with min_periods')
print(amount.rolling(3, min_periods=1).sum())
print('rolling mean')
print(amount.rolling(3).mean())
print('rolling mean with min_periods')
print(amount.rolling(3, min_periods=1).mean())

print(amount.rolling(3, min_periods=1).agg(lambda x: sum(x)))
