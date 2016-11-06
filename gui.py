# -*- coding: utf-8 -*-
#import numpy as np
import core.data_level.mysql as mysql
import matplotlib.pyplot as plt
from tool import count, getN,analysisN

df = mysql.select_basd_on_code('000632')


def run(df):
    ma5_list = df.ma5.tolist()
    lenght = len(ma5_list)
    begin = lenght/2

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
            ana_N.pickN(dt.pre_N)
        pass
    return ana_N.buy,ana_N.sell

buy,sell =run(df)
df.ix[965].ma5

ma5_list = df.ma5.tolist()

x = ma5_list
y = []
z=[]
for i in x:
    y.append(i+1)
for i in x:
    z.append(i-1)
for i in sell:
	y[i]=y[i]-1
for i in buy:
	z[i]=z[i]+1
show = 1
if show == 1:
    # plt.figure(figsize=(8,4))
    plt.plot(x)
    plt.plot(y)
    plt.plot(z)
    plt.xlabel("Time(s)")
    plt.ylabel("Volt")
    plt.title("PyPlot First Example")
    # plt.ylim(-1.2,1.2)
    plt.legend()
    plt.show()
