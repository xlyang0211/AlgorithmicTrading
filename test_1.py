

__author__ = 'xlyang0211'

import tushare as ts
import time
import sqlite3

#  获取股票当日交易信息；
#　print ts.get_hist_data('600000', '2015-11-20', '2015-12-01')
# 获取龙虎榜；
# print ts.top_list('2015-12-01')

# 获取股票基本信息：
#　print ts.get_stock_basics()

# 获取实时数据：
# print ts.get_today_all()

# 获取分笔数据：
#df = ts.get_today_ticks('601333')
#print df.head(10)  # error will reported here;

# 获取大盘指数实时行情：
# df = ts.get_index()
# print df


def calculate_buy_and_sell_side(code, date=None):
    if not date:
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # print "date is: ", date
    df = ts.get_tick_data(code,date)
    buy = 0
    sell = 0
    for data in df.values:
        if data[5] == "买盘":
            buy += data[3]
        elif data[5] == "卖盘":
            sell += data[3]
    print "The buy side sums to: ", buy
    print "The sell side sums to: ", sell
    ratio = float(buy) / sell
    print ratio
    print "Buy/Sell percentage is: %4f %%" % (ratio * 100)

if __name__ == "__main__":
    code_list = {'000697': '炼石有色',
                 '600100': '同方股份',
                 '600198': '大唐电信',
                 '000760': '斯太尔',
                 '600478': '科力远',
                 '601012': '隆基股份',
                 '600599': '熊猫金控',
                 '002295': '精益股份',
                 '600705': '中航资本',
                 '002223': '鱼跃医疗'
                 }
    for key in code_list:
        print "\n" + code_list[key] + ":"
        calculate_buy_and_sell_side(key)