# -*- coding: utf-8 -*-
__author__ = 'xlyang0211'

# 寻找的目标形态是：
# 1. 连续缩量；
# 2. 连续获取当天实时行情，特别注意以下参数：
#       1. 当天大盘的开盘指数；
#       2. 高开的股票；
#       3. 监测股票开盘价，现价，最低值；
#       4. 检测股票与大盘的强弱关系；

import tushare as ts
import datetime
from algorithm_4 import main_4


def read_shrink_code_list(code_list_file):
    F = open(code_list_file, 'r')
    code_list = {}
    shrink_period = 0
    while 1:
        line = F.readline()
        if not line:
            break
        else:
            shrink_period = int(line.strip()[:line.index(':')])
            if shrink_period not in code_list:
                code_list[shrink_period] = []
            code_list[shrink_period].append(line.strip()[line.index(':')+2:])
    F.close()
    return code_list


def check_in_range(self, price_1, price_2, bias):
    price_1 = float(price_1)
    price_2 = float(price_2)
    if price_1 > price_2:
        price_1, price_2 = price_2, price_1
    if (price_2 - price_1) / float(price_1) < bias:
        return True
    else:
        return False


def main_7():
    # main_4(year=2015,
    #        month=12,
    #        day=10,
    #        date_diff=0,
    #        max_shrink_period=10,
    #        min_shrink_period=3,
    #        code_list_file='all_stocks',
    #        result_file='result_file_4')
    code_list = read_shrink_code_list('result_file_4')
    # print "enter here"
    # 上证指数涨幅：
    pd = ts.get_realtime_quotes('sh')
    p_shangzheng = round((float(pd.iloc[0, 1]) - float(pd.iloc[0, 2])) / float(pd.iloc[0, 2]) * 100, 2)
    # 深圳成指涨幅：
    pd = ts.get_realtime_quotes('sz')
    p_shenzhen = round((float(pd.iloc[0, 1]) - float(pd.iloc[0, 2])) / float(pd.iloc[0, 2]) * 100, 2)
    # 中小板：
    pd = ts.get_realtime_quotes('zxb')
    p_zhongxiaoban = round((float(pd.iloc[0, 1]) - float(pd.iloc[0, 2])) / float(pd.iloc[0, 2]) * 100, 2)
    # print "p_shangzheng", p_shangzheng
    # print "p_shenzhen", p_shenzhen
    # print "p_zhongxiaoban", p_zhongxiaoban
    for key in code_list:
        for code in code_list[key]:
            if code[0] == '3':
                continue
            df = ts.get_realtime_quotes(code)
            open = df.iloc[0, 1]
            pre_close = df.iloc[0, 2]
            price = df.iloc[0, 3]
            low = df.iloc[0, 5]
            p_change = round((float(price) - float(pre_close)) / float(pre_close), 2)
            if open > pre_close or low > pre_close:
                # print "p_change", p_change
                print_string = ""
                if open > price:
                    print_string += "高开绿柱，"
                else:
                    print_string += "高开红柱，"
                if code[0] == '6' and p_change > p_shangzheng:
                    print_string += "强于大盘，"
                    print print_string, str(key), code
                elif code[:3] == '000' and p_change > p_shenzhen:
                    print_string += "强于大盘，"
                    print print_string, str(key), code
                elif code[:3] == '002' and p_change > p_zhongxiaoban:
                    print_string += "强于大盘，"
                    print print_string, str(key), code
                else:
                    pass


if __name__ == "__main__":
    main_7()