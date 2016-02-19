# -×- coding: utf-8 -×-
__author__ = 'xlyang0211'

import os
import tushare as ts

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

def read_all_stocks():
    # 读取所有A股代码，并存为'all_stocks'文件；
    if os.path.isfile('all_stocks'):
        pass
    else:
        pd = ts.get_industry_classified()
        F = open('all_stocks', 'w')
        for line in pd.iloc[:, 0]:
            # print line
            F.write(line + "\n")
        F.close()