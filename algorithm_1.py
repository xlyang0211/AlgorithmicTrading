# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

# 本算法计算出连续缩量，并在最近一天跳空高开，振荡（涨幅不高）并放量的股票；

# coding: 'utf-8'
__author__ = 'xlyang0211'

# -*- coding: utf-8 -*-
# __author__ = 'seany'

import tushare as ts
import datetime


class ConsecutiveDecreaseInVolume(object):

    def __init__(self, num_of_days, start_date, code_list_file):
        self.num = num_of_days  # number of days decrease in volume;
        self.start_date = start_date  # what day is it today?
        self.code_list = self.read_code_list(code_list_file)

    def read_code_list(self, code_list_file):
        code_list = []
        F = open(code_list_file, 'r')
        while 1:
            line = F.readline()
            if not line:
                break
            else:
                code_list.append(line.strip())
        return code_list

    def consecutive_decrease(self, stock_code):
        #  寻找连续缩量，最后一天放量的股票，date list比缩量的天数要多一天;
        date_list = self.get_date_list()
        print date_list
        consecutive_day_data = ts.get_hist_data(stock_code, start=str(date_list[0]), end=str(date_list[-1]))
        volume_list = [i for i in consecutive_day_data.iloc[:, 4]]
        if len(volume_list) != len(date_list):
            return None
        close_price_list = [i for i in consecutive_day_data.iloc[:, 2]]
        count = 0
        for i in xrange(len(volume_list) - 2):
            if volume_list[i] > volume_list[i+1]:  #　判断连续缩量
                # if i >= len(volume_list) - 4:
                #     # 获取最后两天股价波动很小，但仍人在缩量的股票：
                #     if self.check_in_range(close_price_list[i], close_price_list[i+1], 0.015):
                #         count += 1
                # else:
                #     count += 1
                count += 1
        if count == len(volume_list) - 2:  # number of consecutive shrink in volume;
            # 获取最有一天跳空高开，放量的股票：
            # print "enter here: ", stock_code
            # print consecutive_day_data.iloc[-2, 2], consecutive_day_data.iloc[-1, 0], consecutive_day_data.iloc[-1, 3]
            if consecutive_day_data.iloc[-1, 0] > consecutive_day_data.iloc[-2, 2] and \
               consecutive_day_data.iloc[-1, 3] > consecutive_day_data.iloc[-2, 2] and \
               consecutive_day_data.iloc[-1, 4] > consecutive_day_data.iloc[-2, 4]:
                print "close: ", consecutive_day_data.iloc[-2, 2]
                print "next open: ", consecutive_day_data.iloc[-1, 0]
                print "next close: ", consecutive_day_data.iloc[-1, 3]
                return stock_code
            else:
                return None
        else:
            return None

    def check_in_range(self, price_1, price_2, bias):
        if price_1 > price_2:
            price_1, price_2 = price_2, price_1
        if (price_2 - price_1) / float(price_1) < bias:
            return True
        else:
            return False

    def get_date_list(self):
        num_list = []
        rdnt = 0
        print "start date is: ", self.start_date
        day_today = self.start_date.weekday() + 1
        print "day_today is: ", day_today
        for i in xrange(self.num + 1):
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
        for i in xrange(self.num + 1):
            date_list = [self.start_date - datetime.timedelta(days=num_list[i])] + date_list
        return date_list

if __name__ == "__main__":
    start_date = datetime.date(2015, 12, 6)
    get_consecutive = ConsecutiveDecreaseInVolume(2, start_date, 'all_stocks')
    F = open('result_algorithm_2', 'w')
    for code in get_consecutive.code_list:
    # if 1:
        # code = '000856'
        de_code = get_consecutive.consecutive_decrease(code)
        if de_code:
            F.write(de_code + "\n")
    F.close()

