# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

import tushare as ts

df = ts.get_realtime_quotes(['000581', '601299'])
print df
print df.iloc[0, 1], df.iloc[0, 2], df.iloc[0, 5]
