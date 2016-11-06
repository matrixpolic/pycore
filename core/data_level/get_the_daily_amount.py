# encoding: utf-8
from multiprocessing.dummy import Pool as ThreadPool
import tushare as ts
import mysql as msl
import pandas as pd
import time
import datetime
from sqlalchemy import create_engine
# import tushare as ts
import pandas as pd
engine = create_engine(
    'mysql://root:@127.0.0.1:3306/stockzen?charset=utf8')

nums1 = msl.select_code_name().code.tolist()
date = msl.select_index('sh').index.tolist()
index = ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']


df = ts.get_tick_data('600848', date='2014-01-09')
df.head(10)
# print df.type
df.to_sql('all_stock_daily_amount_details', engine,
          if_exists='append', index=False)
