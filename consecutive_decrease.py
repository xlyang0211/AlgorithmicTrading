# coding: 'utf-8'
__author__ = 'xlyang0211'

# -*- coding: utf-8 -*-
# __author__ = 'seany'

import tushare as ts
import datetime
import matplotlib


class ConsecutiveDecreaseInVolume(object):

    def __init__(self, num_of_days, day_today, code_list_file):
        self.num = num_of_days  # number of days decrease in volume;
        self.day_today = day_today  # what day is it today?
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
        #  Find num days of consecutive decrease in volume;
        date_list = self.get_date_list()
        # print date_list
        # print type(date_list[0]), type(date_list[-1])
        ten_day_data = ts.get_hist_data(stock_code, start=str(date_list[0]), end=str(date_list[-1]))
        # print ten_day_data.values[0]
        # print ten_day_data
        volume_list = [i[4] for i in ten_day_data.values]
        close_price_list = [i[2] for i in ten_day_data.values]
        # print stock_code, volume_list
        count = 0
        for i in xrange(len(volume_list) - 1):
            if volume_list[i] > volume_list[i+1]:
                if i >= len(volume_list) - 4:
                    if self.check_in_range(close_price_list[i], close_price_list[i+1], 0.015):
                        count += 1
                else:
                    count += 1
        if count == len(volume_list) - 1:
            return stock_code
        else:
            return None

    def check_in_range(self, price_1, price_2, bias):
        if price_1 > price_2:
            price_1, price_2 = price_2, price_1
        if (price_2 - price_1) / float(price_1) < bias:
            return True
        else:
            return False

    def get_date_list(self, start=None):
        num_list = []
        rdnt = 0
        day_today = self.day_today
        for i in xrange(self.num):
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
        if not start:
            start = datetime.date.today()
        for i in xrange(self.num):
            date_list = [start - datetime.timedelta(days=i)] + date_list
        return date_list

if __name__ == "__main__":
    get_consecutive = ConsecutiveDecreaseInVolume(7, 7, 'zixuangu')
    for code in get_consecutive.code_list:
    # if 1:
        # code = '000856'
        de_code = get_consecutive.consecutive_decrease(code)
        if de_code:
            print "code of decrease is: ", de_code