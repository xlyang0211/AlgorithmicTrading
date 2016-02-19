# -*- coding: utf-8 -*-
__author__ = 'xlyang0211'

# 获取的股票形态如下：
# 1. 在指定日期之前连续n天缩量

import tushare as ts
import datetime
import matplotlib


class ConsecutiveDecreaseInVolume(object):

    def __init__(self, max_shrink_period, min_shrink_period, start_date, date_diff, code_list_file):
        self.max_shrink_period = max_shrink_period
        self.min_shrink_period = min_shrink_period
        self.start_date = start_date  # 最后一天的日期；
        self.date_diff = date_diff
        self.code_list = self.read_code_list(code_list_file)
        self.data = {}
        # self.prepare_data()

    def prepare_data(self):
        date_list = self.get_date_list() # 判断第一天缩量的需要；
        print "date list is: ", date_list
        for code in self.code_list:
            self.data[code] = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))

    def read_code_list(self, code_list_file):
        code_list = []
        F = open(code_list_file, 'r')
        while 1:
            line = F.readline()
            if not line:
                break
            else:
                code_list.append(line.strip())
        F.close()
        return code_list

    def consecutive_decrease(self):
        shrink_list = []
        date_list = self.get_date_list() # 判断第一天缩量的需要；
        for code in self.code_list:
            data = ts.get_hist_data(code, start=str(date_list[0]), end=str(date_list[-1]))
            if len(data) != self.max_shrink_period + self.date_diff + 1:
                continue
            volume_list = [i[4] for i in data.values]
            # print stock_code, volume_list
            count = 0
            for i in xrange(self.date_diff, len(volume_list) - 1):
                if volume_list[-i] < volume_list[-(i+1)]:
                    count += 1
                else:
                    break
            if self.min_shrink_period <= count <= self.max_shrink_period:
                print code, volume_list
                shrink_list.append([count, code])
        return shrink_list

    def get_date_list(self):
        num_list = []
        rdnt = 0
        day_today = self.start_date.weekday() + 1
        print "day today is: ", day_today
        for i in xrange(self.max_shrink_period + self.date_diff + 1):
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
            date_list = [self.start_date - datetime.timedelta(days=i)] + date_list
        return date_list


def main_4(year, month, day, date_diff, max_shrink_period, min_shrink_period, code_list_file, result_file):
    start_date = datetime.date(year, month, day) # 想观察的最后一天，一般是今天；
    # date_diff: 缩量的最后一天跟想观察的最后一天之间的差距；
    # max_shrink_period: 需要寻找的最大缩量周期；
    # min_shrink_period: 需要寻找的最小缩量周期；
    # code_list_file: 股票代码文件；
    # result_file: 输出保存文件；
    get_consecutive = ConsecutiveDecreaseInVolume(max_shrink_period, min_shrink_period,
                                                  start_date, date_diff, code_list_file)
    F = open(result_file, 'w')
    code_list = get_consecutive.consecutive_decrease()
    for i in code_list:
        F.write(str(i[0]) + ": ")
        F.write(i[1] + "\n")
    F.close()

if __name__ == "__main__":
    main_4(year=2015,
         month=12,
         day=14,
         date_diff=2,
         max_shrink_period=10,
         min_shrink_period=3,
         code_list_file='all_stocks',
         result_file='algorithm_4_result')
