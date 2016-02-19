# -*- coding: utf8 -*-
__author__ = 'xlyang0211'

# 第一个功能：
# 1. 统计涨停前一天的上涨幅度；
# 2. 统计涨停当天的开盘涨幅：
#    1. 总体统计；
#    2. 区分第几个涨停；
#  3. 统计涨停后第二天的开盘涨幅；


import tushare as ts
import datetime
import math
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os


def read_all_stocks():
    if os.path.isfile('all_stocks'):
        pass
    else:
        pd = ts.get_industry_classified()
        F = open('all_stocks', 'w')
        for line in pd.iloc[:, 0]:
            # print line
            F.write(line + "\n")
        F.close()

def read_code_list(code_list_file):
    # 读取自选股；
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

def calculate_percent_change(code):
    # 对于每一支股票，获取其三个数据；
    change_before_zhangting = defaultdict(int)
    open_at_zhangting = defaultdict(int)
    open_after_zhangting = defaultdict(int)
    data = ts.get_hist_data(code, start='2015-01-01',end=str(datetime.date.today()))
    #print data
    for i in xrange(len(data)):
        # print i
        # print data.iloc[i, 6]
        if data.iloc[i, 6] > 9.9:
            if i != 0:
                # 获取涨停当天的开盘涨幅：
                p_change = (data.iloc[i, 0] - data.iloc[i-1, 2]) / data.iloc[i-1, 2] * 100
                p_change = get_round(p_change)
                open_at_zhangting[p_change] += 1
                # 获取涨停前一天的收盘涨幅：
                p_change = get_round(data.iloc[i-1, 6])
                change_before_zhangting[p_change] += 1
            if i != len(data) - 1:
                # 获取涨停后一天的开盘涨幅：
                p_change = (data.iloc[i+1, 0] - data.iloc[i, 2]) / data.iloc[i, 2] * 100
                p_change = get_round(p_change)
                open_after_zhangting[p_change] += 1
    return change_before_zhangting, open_at_zhangting, open_after_zhangting

def get_round(p_change):
    # 返回floor(p_change)；
    if p_change > 9.9:
        p_change = 10
    elif p_change < -10:
        p_change = -10
    else:
        p_change = int(math.floor(p_change))
    return p_change


def total_statistics(code_list_file):
    statistics_result = dict()
    statistics_result['total'] = {}
    statistics_result['total']['pre'] = defaultdict(int)
    statistics_result['total']['cur'] = defaultdict(int)
    statistics_result['total']['aft'] = defaultdict(int)
    for code in read_code_list(code_list_file):
        statistics_result[code] = {}
        statistics_result[code]['pre'] = {}
        statistics_result[code]['cur'] = {}
        statistics_result[code]['aft'] = {}
        statistics_result[code]['pre'], statistics_result[code]['cur'], \
        statistics_result[code]['aft'] = calculate_percent_change(code)
        # 计算所有的加和统计：
        for key in statistics_result[code]['pre']:
            statistics_result['total']['pre'][key] += statistics_result[code]['pre'][key]
        for key in statistics_result[code]['cur']:
            statistics_result['total']['cur'][key] += statistics_result[code]['cur'][key]
        for key in statistics_result[code]['aft']:
            statistics_result['total']['aft'][key] += statistics_result[code]['aft'][key]
    return statistics_result

if __name__ == "__main__":
    data = {}
    data = total_statistics('all_stocks')
    read_all_stocks()
    while 1:
        code = raw_input("Please input the stock code to consult: ")
        if code:
            stock_data = data[code]
            value_list = []
            max_y = 0
            for key in sorted(stock_data['pre']):
                value_list.append(stock_data['pre'][key])
                if stock_data['pre'][key] > max_y:
                    max_y = stock_data['pre'][key]
            # plt.plot(sorted(stock_data['pre']), value_list, 'rD', linewidth=16)
            plt.plot(sorted(stock_data['pre']), value_list, linewidth=1, marker='o', markersize=10, label='p_change day ahead')
            # print sorted(stock_data['pre'])
            # print value_list
            value_list = []
            for key in sorted(stock_data['cur']):
                value_list.append(stock_data['cur'][key])
                if stock_data['cur'][key] > max_y:
                    max_y = stock_data['cur'][key]
            # plt.plot(sorted(stock_data['cur']), value_list, 'bs', linewidth=16)
            # print sorted(stock_data['cur'])
            # print value_list
            plt.plot(sorted(stock_data['cur']), value_list, linewidth=1, marker='v', markersize=10, label='p_change open today')
            value_list = []
            for key in sorted(stock_data['aft']):
                value_list.append(stock_data['aft'][key])
                if stock_data['aft'][key] > max_y:
                    max_y = stock_data['aft'][key]
            # plt.plot(sorted(stock_data['aft']), value_list, 'gD', linewidth=16)
            # print sorted(stock_data['aft'])
            # print value_list
            plt.plot(sorted(stock_data['aft']), value_list, linewidth=1, marker='d', markersize=10, label='p_change next day')
            l = [-12, 12, 0, max_y + 2]
            plt.axis(l)
            plt.title('Statistics of Zhangting')
            plt.grid(True)
            plt.xticks(np.linspace(-10, 10, 21))
            plt.legend()
            plt.show()
            code = None