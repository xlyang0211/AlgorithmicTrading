# -*- coding: utf-8 -*-
__author__ = 'xlyang0211'


# 本算法用来判断大盘的强势与否，寻找避开弱势（大跌的大盘交易日）；

# 输入：
# 判断的指标（输入）包括：
# 1. 券商启动 --- 大涨？
# 2. 中石油启动 --- 第二天大跌？
# 3. 银行板块启动 --- 救市？第二天怎么走？
# 4. 次新股板块启动 --- 没热点？后面怎么走？
# 5. 眉飞色舞 --- 行情终结还是开始？
# 6. 其他可能的指标；

# 输出：
# 量化的大盘强弱指数（如0～10）和建议仓位（0～10），可以为小数；
# 买什么也作为次要建议给出来；


import logging
import tushare as ts
import datetime

from AlgoPack.AlgoTradeLib import *

if __name__ == "__main__":
    # configure input parameters:
    test_period = 2
    start_date = datetime.date(2016, 2, 24)

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





