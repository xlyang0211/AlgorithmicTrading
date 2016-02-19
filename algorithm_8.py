# -*- coding: utf-8 -*-
# __author__ = 'seany'

# 本算法用来寻找如下形态的股票：
# 1. 正T接着一个倒T；
# 2. 倒T接着一个正T；

# 说明：
# 1. 回测：建议至少进行三个月的回测；
# 2. 回测范围：先在自选股范围回测，如果条件允许测试整个A股；
# 3. 如果运行较快，可以看看尾盘-盘中收益率；否则需要测试开盘-开盘收益率；
# 4. 如果仅仅形态选股无法在随机中脱颖而出，后面的算法就需要考虑以下因素了：
#    1. 分笔成交数据；
#    2. 大盘形态和大盘数据；
#    3. 龙虎榜等非规律性数据；
#    4. 宏观经济因素；
#    5. 板块偏好；

#　积累函数和类库，备做后用；


import sys
import os
import logging
# from AlgoPack.AlgoTradeLib import check_in_range


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# handler2 = logging.FileHandler('hello2.log')
# handler2.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# handler2.setFormatter(formatter)


# add the handlers to the logger

logger.addHandler(handler)
# logger.addHandler(handler2)

logger.debug('Hello baby')


# logging.basicConfig(level=logging.DEBUG, filename='algorithm_8_logging_info')


