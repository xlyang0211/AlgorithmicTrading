# -*- coding: utf-8 -*-
__author__ = 'xlyang0211'


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


import logging
import tushare as ts
import datetime

from AlgoPack.AlgoTradeLib import *

if __name__ == "__main__":
    # configure input parameters:
    test_period = 2
    start_date = datetime.date(2016, 2, 20)

    # configure logging module:
    logging.basicConfig(filename='log_file', level=logging.DEBUG)

    # Get date list:
    date_list = get_date_list(start_date, test_period)

    # Get stock code list to test:
    code_list = read_code_list('all_stocks')
    # code_list = read_code_list('zixuangu1')

    # clear the result file:
    with open('algorithm_9_result', 'w') as result_file:
        pass
    for code in code_list:
        df = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))
        print df
        print type(df.index.tolist())
        if len(df) != 2:
            logging.error(code + ': The data is too less to run the test')
            continue
        else:
            # 长下影线:
            max_value = max(df.values[0][0], df.values[0][2])
            min_value = min(df.values[0][0], df.values[0][2])
            up_line = df.values[0][1] - max_value
            mid = max_value - min_value
            down_line = min_value - df.values[0][3]
            # 长上影线：
            if down_line > 2 * up_line and down_line > 2 * mid:
                max_value = max(df.values[1][0], df.values[1][2])
                min_value = min(df.values[1][0], df.values[1][2])
                up_line = df.values[1][1] - max_value
                mid = max_value - min_value
                down_line = min_value - df.values[1][3]
                # 如果上影线是下影线二倍有余，且今开在昨收1%以内：
                if up_line > 2 * down_line and up_line > 2 * mid:
                    # and check_in_range(df.iloc[1, 0], df.iloc[0, 2], 0.01):
                    with open('algorithm_9_result', 'a') as result_file:
                        result_file.write(code + '\n')
                else:
                    continue
            else:
                continue





