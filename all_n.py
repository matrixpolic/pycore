# coding:utf-8
from multiprocessing.dummy import Pool as ThreadPool
import core.data_level.mysql as mysql
import pandas as pd
from tool import count, getN, analysisN


def run(df, dividor=2):#get  standard N
    ma5_list = df.ma5.tolist()
    lenght = len(ma5_list)
    begin = lenght / dividor

    obj_count = count(df)
    dt = getN(df)
    ana_N = analysisN(df)
    for i in xrange(begin, lenght):
        if i - 1 > 0:
            pre_price = ma5_list[i - 1]
            price = ma5_list[i]

            # obj_count.top_down_resovle(price, pre_price)
            # obj_count.trace(i)
            obj_count.run(i, price, pre_price)

            dic = obj_count.list[-1]
            # print dic
            dt.N_struct_obo(dic)
            # dt.N_rise_struct(dic)
            # dt.N_fall_struct(dic)
            ana_N.pickN(dt.pre_N)#get the standard n
        pass
    return ana_N.dic

def get_all_n(df, dividor=2):
    ma5_list = df.ma5.tolist()
    lenght = len(ma5_list)
    begin = lenght / dividor

    obj_count = count(df)
    dt = getN(df)
    ana_N = analysisN(df)
    for i in xrange(begin, lenght):
        if i - 1 > 0:
            pre_price = ma5_list[i - 1]
            price = ma5_list[i]

            # obj_count.top_down_resovle(price, pre_price)
            # obj_count.trace(i)
            obj_count.run(i, price, pre_price)

            dic = obj_count.list[-1]
            # print dic
            dt.N_struct_obo(dic)
            # dt.N_rise_struct(dic)
            # dt.N_fall_struct(dic)
            #ana_N.pickN(dt.pre_N)#get the standard n
            ana_N.pic_all_N(dt.pre_N)#get all n
        pass
    return ana_N.all_n
    



def resovel_dic(test, df, code):
    result = []
    for i in test:
        Ntype = i['type']
        n1 = i[Ntype][0]
        n2 = i[Ntype][1]
        n3 = i[Ntype][2]
        n4 = i[Ntype][3]
        if n1.has_key("pre_rise_duration"):
            n1_duration = n1['pre_rise_duration']
        else:
            n1_duration = n1['pre_fall_duration']
        if n2.has_key("pre_rise_duration"):
            n2_duration = n2['pre_rise_duration']
        else:
            n2_duration = n2['pre_fall_duration']
        if n3.has_key("pre_rise_duration"):
            n3_duration = n3['pre_rise_duration']
        else:
            n3_duration = n3['pre_fall_duration']
        if n4.has_key("pre_rise_duration"):
            n4_duration = n4['pre_rise_duration']
        else:
            n4_duration = n4['pre_fall_duration']
        result.append([code, Ntype, df.ix[n1['index'] - 1].name, df.ix[n2['index'] - 1].name, df.ix[
                      n3['index'] - 1].name, df.ix[n4['index'] - 1].name, n1_duration, n2_duration, n3_duration, n4_duration])

    return result



def insert_to_tb(result,table="all_N_struct"):

    # Ndetail = pd.DataFrame(columns=("code", "type", "n1", "n2", "n3",
    #                                 "n4", "n1_duration", "n2_duration", "n3_duration", "n4_duration"))
    # for i in xrange(0, len(result)):
    #     Ndetail.loc[i] = result[i]
    #info=mysql.insert_tab(Ndetail, "N_struct")
    mysql.insert_tab(result, table)
    #print info
    return result

#mysql.insert_tab(Ndetail, "N_struct")
#去除重复的N型
def result_filter(result,old_df):
    
    new=result.n4.tolist()
    print new
    old=old_df.n4.tolist()
    print old
    insert= [i for i in new if i in old]
    print insert
    # eresult.loc[result['n4']==insert[0]]=[None,None,None,None,None,None,None,None,None,None]
    # print result.loc[result['n4']==insert[0]]
    for i in insert:
        result.loc[result['n4']==i]=[None,None,None,None,None,None,None,None,None,None]
    # print result.dropna()
    return result.dropna()


def total_run(code,n_table="N_struct"):
    df = mysql.select_basd_on_code(code)
    #test = run(df, 2)#get all standard n
    test=get_all_n(df,2)
    result = resovel_dic(test, df, code)

    Ndetail = pd.DataFrame(columns=("code", "type", "n1", "n2", "n3",
                                    "n4", "n1_duration", "n2_duration", "n3_duration", "n4_duration"))
    for i in xrange(0, len(result)):
        Ndetail.loc[i] = result[i]
    #info=mysql.insert_tab(Ndetail, "N_struct")
    old_df=mysql.select_without_index(n_table,code," ")
    # print old_df
    filter_data=result_filter(Ndetail, old_df)

    # print filter_data
    n = insert_to_tb(filter_data,n_table)
    return n

# n=total_run('600166')


codes = mysql.select().code.tolist()
end_date = mysql.select_index('sh').ix[-1].name
already_codes = mysql.select_day_mark(end_date).code.tolist()
result = [i for i in codes if i not in already_codes]

# for i in codes:

#     total_run(i)


# total_run("600123")

def pool_func(func_name, ls,num=30):
    pool = ThreadPool(num)
    results = pool.map(func_name, ls)
    pool.close()
    pool.join()
    return results

pool_func(total_run, result)





