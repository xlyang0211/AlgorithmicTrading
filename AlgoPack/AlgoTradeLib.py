# -*- coding: utf-8 -*-
# __author__ = 'seany'

import tushare as ts
import datetime


def get_date_list(start_date, number_of_days):
    """
    输入起始时间和查询的天数，返回交易从起始日期起连续交易的天数
    1. 函数会自动跳过周末；
    2. 函数无法跳过非周末的节假日；
    :param start_date: start_date = datetime.date(2015, 12, 8)，是datetime.date数据格式；
    :param number_of_days: 你需要查询的天数；
    :return: 返回date格式的日期构成的list；
    """
    num_list = []
    rdnt = 0
    day_today = start_date.weekday() + 1
    for i in xrange(number_of_days):
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


def check_in_range(price_1, price_2, bias):
    """
    检查price_2是否在price_1的某个允许误差内，该误差即bias；
    :param price_1: 数据1，基准数据，整数或浮点数都可以；
    :param price_2: 数据2，比较数据，整数或浮点数都可以；
    :param bias: 指定允许的偏差；
    :return: 如果数据2在数据1的允许偏差内，返回True，否则返回False;
    """
    price_1 = float(price_1)
    price_2 = float(price_2)
    if price_1 > price_2:
        price_1, price_2 = price_2, price_1
    if (price_2 - price_1) / float(price_1) < bias:
        return True
    else:
        return False


def read_shrink_code_list(code_list_file):
    """
    一种code_list_file是寻找连续缩量的股票的输出文件，文件内容是：
    stock_code: number_of_consecutive_shrink_day
    :param code_list_file: 保存输入股票代码的文件；
    :return: 返回保存文件信息的哈希，
    """
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


def read_code_list(code_list_file):
    """
    读取一般的保存股票代码的文件
    :param code_list_file: 股票代码输入文件；
    :return: 返回股票代码的list
    """
    code_list = []
    F = open(code_list_file, 'r')
    while 1:
        line = F.readline()
        if not line:
            break
        else:
            code_list.append(line.strip())
    return code_list


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
        date_list = get_date_list() # 判断第一天缩量的需要；
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
        date_list = get_date_list() # 判断第一天缩量的需要；
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


def ConfigureConsecutiveDecreaseInVolume(year, month, day, date_diff, max_shrink_period, min_shrink_period,
                                         code_list_file, result_file):
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
