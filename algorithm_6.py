# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

# 寻找的目标形态是：
# 首先一直缩量，然后：
# 第一天：波动很小的十字，继续缩量；
# 第二天：光头短红柱，略放量；
# 第三天：同第一天；
# 预计：第四天将要拉升了；

import tushare as ts
import datetime
# from collections import defaultdict

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

def get_date_list(start_date):
    num_list = []
    rdnt = 0
    day_today = start_date.weekday() + 1
    for i in xrange(3):
        if day_today == 6:
            rdnt += 1
            num_list.append(i + rdnt)
            day_today = 5  # if it's saturday, adjust it to friday;
        elif day_today == 7:
            rdnt += 2
            num_list.append(i + rdnt)
            day_today = 5  # if it's Sunday, adjust it to friday;
        else:
            num_list.append(i + rdnt)
        day_today -= 1
        if day_today == 0:
            day_today = 7
    date_list = []
    for i in num_list:
        date_list = [start_date - datetime.timedelta(days=i)] + date_list
    return date_list

def check_in_range(self, price_1, price_2, bias):
    price_1 = float(price_1)
    price_2 = float(price_2)
    if price_1 > price_2:
        price_1, price_2 = price_2, price_1
    if (price_2 - price_1) / float(price_1) < bias:
        return True
    else:
        return False

def select_shape():
    code_list = {}
    ret = []
    date_list = []
    start_date = datetime.date(2015, 12, 8)
    date_list = get_date_list(start_date)
    print date_list
    code_list = read_shrink_code_list('algorithm_4_result')
    day_1 = []
    day_2 = []
    day_3 = []
    for key in code_list:
        for code in code_list[key]:
            print "code is: ", code
            data = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))
            if len(data) != 3:
                continue
            # 已经知道第一天是缩量的了，判断第二天和第三天的量：
            if data.iloc[1, 4] > data.iloc[0, 4] and data.iloc[1, 4] > data.iloc[2, 4]:
                # 判断第一天的形态：
                if check_in_range(data.iloc[0, 0], data.iloc[0, 2], 0.005) and \
                   data.iloc[0, 1] > max(data.iloc[0, 0], data.iloc[0, 2]) and \
                   data.iloc[0, 3] < min(data.iloc[0, 0], data.iloc[0, 2]):
                    day_1.append(code)
                    # 判断第二天的形态：
                    if data.iloc[1, 3] <= data.iloc[1, 0] <= data.iloc[1, 1] and \
                       data.iloc[1, 0] < data.iloc[1, 2] <= data.iloc[1, 1]:
                        day_2.append(code)
                        # 判断第三天的形态：
                        if check_in_range(data.iloc[0, 0], data.iloc[0, 2], 0.005) and \
                           data.iloc[0, 1] > max(data.iloc[0, 0], data.iloc[0, 2]) and \
                           data.iloc[0, 3] < min(data.iloc[0, 0], data.iloc[0, 2]):
                            ret.append([key, code])
    print "day_1 is: ", day_1
    print "day_2 is: ", day_2
    for i in ret:
        print i

if __name__ == "__main__":
    select_shape()