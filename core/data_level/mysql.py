from sqlalchemy import create_engine
# import tushare as ts
import pandas as pd


engine = create_engine(
    'mysql://root:root@127.0.0.1:3306/stock_zen?charset=utf8')

def insert_sh_5mins(df):
    df.to_sql('sh5mins', engine,
              if_exists='append')


def insert(num, df):
    # df = ts.get_hist_data(str(num))
    sql = "select * from " + "`" + str(num) + "`"

    try:
        df.to_sql(str(num), engine, if_exists='append')
    except Exception, e:
        print e
        df.to_sql(str(num), engine, if_exists='append')
    # else:
    #    pass
    finally:
        test = pd.read_sql(sql, engine, index_col='date')
        if test.empty is True:
            print 'This %s is not successfull' % num
'''
INSERT FUNCTION
'''
def insert_tab(df,table):
    try:
        df.to_sql(table, engine,
                  if_exists='append', index=False)
    except Exception, e:
        print e
        df.to_sql(table, engine,
                  if_exists='append', index=False)
    finally:

        return "check"


def insert_dayline_details(df):
    df.to_sql('all_stock_dayline_details', engine,
              if_exists='append', index=False)


def update(df):
    try:
        df.to_sql('all_stock_dayline_details', engine,
              if_exists='append', index=False)
    except Exception, e:
        print e
    finally:
        return "check",df.index[-1]
'''
SELECT FUNCTION
'''
def select_day_mark(date='2016-03-22'):
    sql="SELECT * FROM stock_zen.day_mark where date='"+ date +"'"
    test = pd.read_sql(sql, engine)
    return test

def select_trend(table="stock_trend",code="600123"):
    sql = "SELECT * FROM "+"`"+table+"`"+"WHERE `code` = "+str(code)+" order by 'index'"
    test = pd.read_sql(sql, engine, index_col='index')
    return test

def select_without_index(table='test_table',code='600123',condition=" ORDER BY date ASC"):
    sql = "SELECT * FROM "+"`"+table+"`"+" WHERE `code` = '"+str(code)+"'"+condition
    test = pd.read_sql(sql, engine)
    return test

def select_with_index(table='test_table',code='600123'):
    sql = "SELECT * FROM "+"`"+table+"`"+" WHERE `code` = '"+str(code)+"'"+" ORDER BY date ASC"
    test = pd.read_sql(sql, engine,index_col="date")
    return test


def select():
    sql = "SELECT * FROM code_classification"
    test = pd.read_sql(sql, engine, index_col='index')
    return test

def select_code_name():
    sql = "SELECT * FROM code_name_info"
    test = pd.read_sql(sql, engine, index_col='index')
    return test


def select_basd_on_code(num):
    # The mysql requre the formate below to improve the performance
    sql = "SELECT * FROM `all_stock_dayline_details` WHERE `code` = " + \
        "'" + str(num).zfill(6) + "'" + \
        " ORDER BY `all_stock_dayline_details`.`date` ASC "
    results = pd.read_sql(sql, engine, index_col='date')
    return results


def select_index(index):
    sql = "SELECT * FROM `all_stock_dayline_details` WHERE `code` = " + \
        "'" + index + "'" + "ORDER BY `all_stock_dayline_details`.`date` ASC"
    results = pd.read_sql(sql, engine, index_col='date')
    return results


def select_index_basd_on_date(index, date):
    sql = "SELECT * FROM `all_stock_dayline_details` WHERE `code` = " + \
        "'" + index + "'" + "and `date`=" + "'" + str(date) + "'"
    results = pd.read_sql(sql, engine, index_col='date')
    return results


def select_basd_on_date(num, date):
    # The mysql requre the formate below to improve the performance
    sql = "SELECT * FROM `all_stock_dayline_details` WHERE `code` = " + \
        "'" + str(num).zfill(6) + "'" + "and `date`=" + "'" + str(date) + "'"
    results = pd.read_sql(sql, engine, index_col='date')
    return results
