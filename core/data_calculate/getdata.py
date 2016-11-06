from ..data_level import multprocess_stock as pl
from ..data_level import mysql as mysql
from zen_data_result import zen_trend
import time
import talib as ta
import pandas as pd
import datetime



class getdata(object):
    """docstring for getdata"""

    def __init__(self, code='600123'):
        pl.get_today_data(code)
        self.pl = 1


# test=getdata('600123')
class getdetail(zen_trend):
    """docstring for getdetail"""

    def __init__(self, code):
        self.flag = 1
        self.code = code
        self.old_top_bottom_return = mysql.select_without_index(
            table='test_table', code=self.code).sort_index()
        self.old_trend_return = mysql.select_trend(
            code=self.code).sort_values(['end'])
        # date=self.old_trend_return.iloc[-1].end
        if 'self.df' not in locals():
            self.df = mysql.select_index(self.code)[-120:]
            self.test = self.stock_ana_test()
            self.mark_result_return = self.mark_result()
            #self.total_cal_return = self.total_cal()
            self.trend_source = self.mark_result_filter_test()
            self.top_bottom_return = self.top_bottom()
            #??problem here
            self.trend_return = self.trend()

        if self.old_trend_return.iloc[-1].end == self.trend_return.iloc[-1].end:
            self.flag = 0

        self.begin = self.trend_return.loc[self.trend_return[
            'end'] == self.old_trend_return.iloc[-1].end]
        if(len(self.begin) == 1):
            # print 'this------',self.code
            self.insert_trend_return = self.trend_return[
                int(self.begin['index']) + 1:]
        elif(self.begin.empty is True):
            self.flag = 0
            pass
        else:
            print 'this------', self.code
            self.insert_trend_return = self.trend_return[
                int(self.begin.iloc[-1]['index']) + 1:]

        #t1 = time.strptime(odate, "%Y-%m-%d")
        #t2 = time.strptime(ndate, "%Y-%m-%d")
        #trend_return last end date is before the old_trend_return end date
        if time.mktime(time.strptime(self.trend_return.iloc[-1].end, "%Y-%m-%d")) < time.mktime(time.strptime(self.old_trend_return.iloc[-1].end, "%Y-%m-%d")):
            self.coordinate_trend=self.old_trend_return
        else:
            self.coordinate_trend=self.trend_return

        #self.rough_trend_return = self.rough_trend()

    def rsi(self):
        self.rsi = ta.RSI(self.df['close'].values)

    def coordinate(self):
        # find=self.df.index.tolist()

        df = pd.DataFrame(
            columns=('type', 'date', 'code', 'mark_low', 'mark_high'))
        mark = self.coordinate_trend.iloc[-1]
        beg = mark.begin
        end = mark.end
        # print find.index(beg),find.index(end),self.df.ix[beg]
        if(mark.key == 'fall'):
            mark_high = self.df.ix[beg].high
            mark_low = self.df.ix[end].low
        else:
            mark_high = self.df.ix[end].high
            mark_low = self.df.ix[beg].low

        cp_low = self.df.ix[-1].low
        cp_high = self.df.ix[-1].high
        # print mark_low,cp_low
        if(float(cp_high) > float(mark_high)):
            #print ['high',self.df.ix[-1].name,self.code,mark_low,mark_high,cp_high]
            df.loc[1] = ['high', self.df.ix[-1].name,
                         self.code, mark_low, mark_high]
            result = ['high', self.df.ix[-1].name,
                      self.code, mark_low, mark_high]
        elif(cp_low < mark_low):
            #print ['low',self.df.ix[-1].name,self.code,mark_low,mark_high]
            df.loc[1] = ['low', self.df.ix[-1].name,
                         self.code, mark_low, mark_high]
            result = ['low', self.df.ix[-1].name,
                      self.code, mark_low, mark_high]
        elif(cp_high < mark_low):
            #print ['ab_low',self.df.ix[-1].name,self.code,mark_low,mark_high]
            df.loc[1] = ['ab_low', self.df.ix[-1].name,
                         self.code, mark_low, mark_high]
            result = ['ab_low', self.df.ix[-1].name,
                      self.code, mark_low, mark_high]
        elif(cp_low > mark_high):
            #print ['ab_high',self.df.ix[-1].name,self.code,mark_low,mark_high]
            df.loc[1] = ['ab_high', self.df.ix[-1].name,
                         self.code, mark_low, mark_high]
            result = ['ab_high', self.df.ix[-1].name,
                      self.code, mark_low, mark_high]
        else:
            #print ['jump',self.df.ix[-1].name,self.code,mark_low,mark_high]
            df.loc[1] = ['jump', self.df.ix[-1].name,
                         self.code, mark_low, mark_high]
            result = ['jump', self.df.ix[-1].name,
                      self.code, mark_low, mark_high]
        self.df_coordinate = df
        return result


# a=getdetail('300436')
# codes=mysql.select().code.tolist()
# test=[]
# for i in codes[:1]:
#     test.append(getdetail(i))

# for i in test:
#     a=i.coordinate()

# mysql.insert_tab(a,'day_mark')


# print test.rough_trend_return[-3:-2]['rel_index'].tolist()[0].split(",")
# print test.g_df.index.tolist().index(test.g_top_bottom.date.tolist()[-1])
# print len(test.g_df.index.tolist())

# print test.g_top_bottom.date.tolist()[-1]
# print test.g_df.ix[test.g_top_bottom.date.tolist()[-1]]
# date_list = test.df.index.tolist()
