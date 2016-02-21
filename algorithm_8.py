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
import tushare as ts
import datetime

from AlgoPack.AlgoTradeLib import *

if __name__ == "__main__":
    # configure input parameters:
    test_period = 90
    start_date = datetime.date(2016, 2, 20)

    # configure logging module:
    logging.basicConfig(filename='log_file', level=logging.DEBUG)

    # Get date list:
    date_list = get_date_list(start_date, test_period)

    # Get stock code list to test:
    code_list = read_code_list('all_stocks')
    # code_list = read_code_list('zixuangu1')

    # clear the result file:
    with open('algorithm_8_result', 'w') as result_file:
        pass
    for code in code_list:
        df = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))
        print df
        print type(df.index.tolist())
        if len(df) < 4:
            logging.warning(code + ': The data is too less to run the test')
            continue
        else:
            for i in xrange(0, len(df)-3):
                # 长下影线:
                print date_list[i]
                max_value = max(df.values[i][0], df.values[i][2])
                min_value = min(df.values[i][0], df.values[i][2])
                up_line = df.values[i][1] - max_value
                mid = max_value - min_value
                down_line = min_value - df.values[i][3]
                # 如果下影线是上影线的二倍有余：
                if down_line > 2 * up_line and down_line > 2 * mid:
                    max_value = max(df.values[i+1][0], df.values[i+1][2])
                    min_value = min(df.values[i+1][0], df.values[i+1][2])
                    up_line = df.values[i+1][1] - max_value
                    mid = max_value - min_value
                    down_line = min_value - df.values[i+1][3]
                    # 如果上影线是下影线二倍有余，且今开在昨收1%以内：
                    if up_line > 2 * down_line and up_line > 2 * mid and \
                            check_in_range(df.iloc[i+1, 0], df.iloc[i, 2], 0.1):
                        with open('algorithm_8_result', 'a') as result_file:
                            result_file.write(code + " at " + str(df.index.tolist()[i]) + ": ")
                            # print type(df.iloc[i+2, 2].item())
                            # print type(df.iloc[i+1, 2].item())
                            first_day_close = df.iloc[i+1, 2].item()
                            second_day_close = df.iloc[i+2, 2].item()
                            second_day_open = df.iloc[i+2, 0].item()
                            third_day_open = df.iloc[i+3, 0].item()
                            earning_1 = 100 * (df.iloc[i+2, 2].item() - df.iloc[i+1, 2].item())/df.iloc[i+1, 2].item()
                            earning_2 = 100 * (df.iloc[i+3, 0].item() - df.iloc[i+2, 0].item())/df.iloc[i+2, 0].item()
                            bias = 0
                            if code[0] == '6':  # 上证
                                df_1 = ts.get_hist_data('sh', start=str(date_list[i+2]), end=str(date_list[i+2]))
                                if len(df_1) == 0:
                                    continue
                                bias = 100 * (df_1.iloc[0, 2].item() - df_1.iloc[0, 0].item()) / df_1.iloc[0, 0].item()
                            elif code[0] == '0':
                                df_1 = ts.get_hist_data('sz', start=str(date_list[i+2]), end=str(date_list[i+2]))
                                if len(df_1) == 0:
                                    continue
                                bias = 100 * (df_1.iloc[0, 2].item() - df_1.iloc[0, 0].item()) / df_1.iloc[0, 0].item()
                            # earning_1 -= bias
                            # earning_2 -= bias
                            if bias >= 3:
                                result_file.write("\nWarning: Big crash in the market")
                            result_file.write("\nnext day close - current day close: %f%%" % earning_1)
                            result_file.write("\n3rd day open - 2nd day open: %f%%\n\n" % earning_2)
                    else:
                        continue
                else:
                    continue





