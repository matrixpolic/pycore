import pandas as pd


class macd():

    """macd calculate"""
    df = None
    index_list = list()
    '''dic12 = dict()
    dic26 = dict()
    dicDIF = dict()
    dicEDA = dict()
    '''

    def __init__(self, df):
        # super(macd, self).__init__()
        self.df = df
        self.index_list = df.index
        self.dic12 = self.EMA_colculate(12)
        self.dic26 = self.EMA_colculate(26)
        self.dicDIF = self.DIF_coculate(self.dic12, self.dic26)
        self.dicEDA = self.EDA_coculate()
        self.results = pd.DataFrame()
        self.results['EDA'] = pd.Series(self.dicEDA)
        self.results['DIF'] = pd.Series(self.dicDIF)
        self.results['12'] = pd.Series(self.dic12)
        self.results['26'] = pd.Series(self.dic26)
        self.results['bar'] = pd.Series(self.BAR_coculate())

    def EMA_colculate(self, n, list_num=4):
        data = self.df.ix[:, list_num]
        dic = dict()
        for i in xrange(0, len(self.index_list)):
            if i == 0:
                y = data.ix[i]
                dic[self.index_list[i]] = y
            else:
                # print y
                y = y * (n - 1) / (n + 1) + 2 * (data.ix[i]) / (n + 1)
            # print str(i) + "------"
                dic[self.index_list[i]] = y
            # print y
        return dic

    def EMA(self, date, n12, n26):
        return n12.get(date) - n26.get(date)

    def DIF_coculate(self, n12, n26):
        # data = df.ix[:, 2]
        dic = dict()
        for i in xrange(0, len(self.index_list)):
            dic[self.index_list[i]] = self.EMA(self.index_list[i], n12, n26)
        # print y
        return dic

    def EDA_coculate(self, n=9):
        dic = self.dicDIF
        dic_EDA = dict()
        for i in xrange(0, len(self.index_list)):
            if i == 0:
                y = dic.get(self.index_list[i])
                dic_EDA[self.index_list[i]] = y
            else:
                y = y * (n - 1) / (n + 1) + 2 * \
                    dic.get(self.index_list[i]) / (n + 1)
                dic_EDA[self.index_list[i]] = y
            # dic[index_list[i]] = EMA(index_list[i], n12, n26)
            # print y
        return dic_EDA

    def BAR_coculate(self):
        bar = dict()
        for i in xrange(0, len(self.index_list)):
            date = self.index_list[i]
            bar[date] = self.dicDIF.get(date) - self.dicEDA.get(date)
        return bar
'''
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from numpy.random import randn
from sqlalchemy import create_engine
# import tushare as ts
engine = create_engine(
    'mysql://root:@127.0.0.1:3306/stockzen?charset=utf8')
sql = "select * from sh limit 90"
df = pd.read_sql(sql, engine, index_col='date')
# x = df.ix[:, 2]
#index_list = list(df.index)

test = macd(df)
'''
