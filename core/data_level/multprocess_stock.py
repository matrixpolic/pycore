from multiprocessing.dummy import Pool as ThreadPool
import tushare as ts
import mysql as msl
import pandas as pd
import time
import datetime

nums1 = list(msl.select().index)
index = ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']

def get_sh_5mins():
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    df=ts.get_hist_data('sh', ktype='5',start='2016-01-09',end=end_date)
    msl.insert_sh_5mins(df)


def get_hist_data(num):
    df = ts.get_hist_data(num, retry_count=10)
    if df is None:
        print num
    else:
        df['code'] = num
        df['date'] = pd.Series(df.index, index=df.index)
        msl.insert_dayline_details(df)
        return {num: df}


def get_today_data(num):
    # date = time.strftime('%Y-%m-%d', time.localtime())
    # print num
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # start_date = select_index('sh').ix[-1].name
    start_date_timesrtucture = datetime.datetime.strptime(
        msl.select_basd_on_code(num).ix[-1].name, "%Y-%m-%d") + datetime.timedelta(1)
    start_date = start_date_timesrtucture.strftime('%Y-%m-%d')
    # print end_date, start_date

    if datetime.datetime.now().date() < start_date_timesrtucture.date():
        print "today complete update"
        return "today complete update"
    # print start_date, end_date
    if msl.select_basd_on_date(num, start_date).empty is True:
        print start_date, end_date, num
        df = ts.get_hist_data(num, start=start_date, end=end_date)
        if df.empty is True:
            return {num: None}
        else:
            df['code'] = num
            df['date'] = pd.Series(df.index, index=df.index)
            print df.ix[0], df.ix[-1]
            msl.update(df)
            return {num: df}
    else:
        print 'This day already has date', start_date, index
        return 'This day already has date'


def get_index_data(index):
    # date = time.strftime('%Y-%m-%d', time.localtime())
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    start_date_timesrtucture = datetime.datetime.strptime(
        msl.select_index(index).ix[-1].name, "%Y-%m-%d") + datetime.timedelta(1)
    start_date = start_date_timesrtucture.strftime('%Y-%m-%d')
    if datetime.datetime.now().date() < start_date_timesrtucture.date():
        print "today complete update"
        return "today complete update"
    if msl.select_index_basd_on_date(index, start_date).empty is True:
        print start_date, end_date, index
        df = ts.get_hist_data(index, start=start_date, end=end_date)
        if df.empty is True:
            return {index: None}
        else:
            df['code'] = index
            df['date'] = pd.Series(df.index, index=df.index)
            msl.update(df)
            print df
            return {index: df}
    else:
        print 'This day already has date', start_date, index
        return 'This day already has date'

'''
pool = ThreadPool(30)
# Open the urls in their own threads
# and return the results
# results = pool.map(get_today_data, nums1)
results = pool.map(get_hist_data, index)
# close the pool and wait for the work to finish
pool.close()
pool.join()
datetime.datetime.strptime(select_index('sh').ix[-1].name, "%Y-%M-%d") + datetime.timedelta(1)
'''


def update_based_on_time():
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # start_date = select_index('sh').ix[-1].name
    start_date = (datetime.datetime.strptime(msl.select_index(
        'sh').ix[-1].name, "%Y-%m-%d") + datetime.timedelta(1)).strftime('%Y-%m-%d')
    return start_date, end_date


def pool_func(func_name, ls,num=30):
    pool = ThreadPool(num)
    results = pool.map(func_name, ls)
    pool.close()
    pool.join()
    return results
