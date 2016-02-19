# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

# 本算法计算出连续缩量，并在最近一天跳空高开，振荡（涨幅不高）并放量的股票；

# coding: 'utf-8'
__author__ = 'xlyang0211'

# -*- coding: utf-8 -*-
# __author__ = 'seany'

import tushare as ts
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class ConsecutiveDecreaseInVolume(object):

    def __init__(self, max_recall_period, start_date, end_date, code_list_file):
        self.max_recall_period = max_recall_period
        self.start_date = start_date
        self.end_date = end_date
        self.code_list_file = code_list_file
        self.code_list = self.read_code_list()
        self.all_data = {}

        self.prepare_date()

    def prepare_date(self):
        for code in self.code_list:
            self.all_data[code] = {}
            self.all_data[code]['open'] = []  # 开盘价
            self.all_data[code]['high'] = []  # 最高价；
            self.all_data[code]['close'] = []  # 收盘价
            self.all_data[code]['low'] = []  # 最低价；
            self.all_data[code]['volume'] = []  # 成交量；

            consecutive_day_data = ts.get_hist_data(code, start=str(self.start_date), end=str(self.end_date))
            # print consecutive_day_data.iloc[:, 0]
            self.all_data[code]['open'] = consecutive_day_data.iloc[:, 0]
            # print self.all_data[code]['open'][1]
            self.all_data[code]['high'] = consecutive_day_data.iloc[:, 1]
            self.all_data[code]['close'] = consecutive_day_data.iloc[:, 2]
            self.all_data[code]['low'] = consecutive_day_data.iloc[:, 3]
            self.all_data[code]['volume'] = consecutive_day_data.iloc[:, 4]

    def read_code_list(self):
        code_list = []
        F = open(self.code_list_file, 'r')
        while 1:
            line = F.readline()
            if not line:
                break
            else:
                code_list.append(line.strip())
        return code_list

    def consecutive_decrease_and_increase(self, shrink_period):
        #  寻找连续缩量，最后一天放量的股票，date list比缩量的天数要多一天;
        p_profit_list_open = []
        p_profit_list_close = []
        for code in self.code_list:
            date_length = len(self.all_data[code]['open'])
            if date_length < shrink_period + 3:
                continue
            for i in xrange(shrink_period + 1, date_length - 1):
                count = 0
                for j in xrange(i - shrink_period - 1, i- 1):
                    if self.all_data[code]['volume'][j] > self.all_data[code]['volume'][j+1]:  # 缩量
                        count += 1
                if count == shrink_period - 1:  # 连续缩量备选；
                    if i - shrink_period - 1 != 0 and \
                       self.all_data[code]['volume'][i] < self.all_data[code]['volume'][i-1]:
                        continue  # 这种情况属于更高的连续缩量的情况；
                    # 如果：跳空高开，最低也高于前一天收盘，并且放量（这在尾盘是可以看到的）
                    if self.all_data[code]['open'][i] > self.all_data[code]['close'][i-1]:
                        # 获取后一天的开盘涨幅：
                        p_profit_open = (self.all_data[code]['open'][i+1] - self.all_data[code]['open'][i])/self.all_data[code]['open'][i]
                        p_profit_open = round(100 * p_profit_open, 2)
                        p_profit_close = (self.all_data[code]['close'][i+1] - self.all_data[code]['open'][i])/self.all_data[code]['open'][i]
                        p_profit_close = round(100 * p_profit_close, 2)
                        p_profit_list_open.append(p_profit_open)
                        p_profit_list_close.append(p_profit_close)
        return p_profit_list_open, p_profit_list_close

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
    # start_date = [2015, 8, 26]
    #　end_date = [2015, 12, 6]
    algorithm_2_result_file = 'algorithm_2_result_file'
    start_date = datetime.date(2015, 8, 26)
    end_date = datetime.date(2015, 12, 6)
    code_list_file = 'all_stocks'
    max_recall_period = 13  # 最大缩量周期
    get_consecutive = ConsecutiveDecreaseInVolume(max_recall_period, start_date, end_date, code_list_file)
    F = open('algorithm_3_result_file', 'w')
    F.write("%20s: %10s%10s\n" % ('shrink_period', 'mean', 'var'))
    for shrink_period in xrange(max_recall_period, 1, -1):  # 缩量周期；13到2；
        print 'enter here!!!'
        open_list = []
        close_list = []
        open_list, close_list = get_consecutive.consecutive_decrease_and_increase(shrink_period)
        if len(open_list):
            open_mean = round(np.mean(open_list), 4)
            open_var = round(np.var(open_list), 4)
            x = np.arange(-10, 10, 0.01)
            y = stats.norm.pdf(x, open_mean, open_var)
            plt.plot(x, y, color='b', label='open')
            F.write("%20d: %10s%10s\n" % (shrink_period, str(open_mean), str(open_var)))
        if len(close_list):
            close_mean = round(np.mean(close_list), 4)
            close_var = round(np.var(close_list), 4)
            x = np.arange(-10, 10, 0.01)
            y = stats.norm.pdf(x, close_mean, close_var)
            plt.plot(x, y, color='k', label='close')
            F.write("%20d: %10s%10s\n" % (shrink_period, str(close_mean), str(close_var)))
        plt.subplot(3, 4, 14 - shrink_period)
    F.close()
    plt.show()