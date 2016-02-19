# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

# 寻找的目标形态是：
# 首先一直缩量，然后：
# 最后一天收长上影线并放量；

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
    for i in xrange(2):
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

def get_long_up_shadow_line():
    code_list = {}
    ret = []
    date_list = []
    start_date = datetime.date(2015, 12, 9)
    date_list = get_date_list(start_date)
    print date_list
    code_list = read_shrink_code_list('algorithm_4_result_2')
    for key in code_list:
        for code in code_list[key]:
            #print "code is: ", code
            data = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))
            if len(data) != 2:
                continue
            #print "enter here"
            #print data
            ##print data.iloc[0, 4], data.iloc[1, 4]
            print round(data.iloc[0, 4]/data.iloc[1, 4], 2)
            if data.iloc[0, 4] < 1.2 * data.iloc[1, 4]:  # 放量；
                #print data
                print code
                down_shadow_line = min(data.iloc[1, 2], data.iloc[1, 0]) - data.iloc[1, 3]
                up_shadow_line = data.iloc[1, 1] - max(data.iloc[1, 2], data.iloc[1, 0])
                p_up = up_shadow_line / data.iloc[1, 1]
                if p_up > 0.03:
                    ret.append(["1", code])
                mid = max(data.iloc[1, 2], data.iloc[1, 0]) - min(data.iloc[1, 2], data.iloc[1, 0])
                if up_shadow_line > 2 * down_shadow_line and up_shadow_line > 2 * mid:
                    ret.append(["2", code])
    print ret

if __name__ == "__main__":
    get_long_up_shadow_line()