#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from ..data_level import mysql as mysql
import time
from datetime import datetime
from matplotlib.dates import date2num
from ..data_calculate.stock_data_analysis_mod import data_analysis
def show():
	code = '600123'
	test = data_analysis(code)
	# l=zen_result_test(code)
	# l=zen_result(code)
	l = test.mark_result_return
	# l=test.total_cal_return
	# l=mark_result_filter(code)
	df = mysql.select_index(code)

	lis = list()

	for i in range(0, len(df.index)):
	    #a = time.mktime(time.strptime(df.ix[i].name, '%Y-%m-%d'))
	    date = time.strptime(df.ix[i].name, '%Y-%m-%d')
	    a = datetime(date.tm_year, date.tm_mon, date.tm_mday)
	    lis.append((date2num(a), df.ix[i].open, df.ix[
	               i].high, df.ix[i].low, df.ix[i].close))

	flag = list()
	for f in l:
	    i = f[0].values()[0]
	    att = f[0].keys()[0]
	    date = time.strptime(i.name, '%Y-%m-%d')
	    flag_date = datetime(date.tm_year, date.tm_mon, date.tm_mday)
	    flag.append((date2num(flag_date), i.open,
	                 i.high, i.low, i.close, i.name, att))

	#plt.figure(figsize=(20, 6), dpi=80)

	# mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	# alldays = DayLocator()              # minor ticks on the days
	# weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	# dayFormatter = DateFormatter('%d')      # e.g., 12

	#quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)
	# print lis[:50]

	quotes = lis
	fig, ax = plt.subplots()

	candlestick_ohlc(ax, quotes, width=0.5)
	ax.xaxis_date()
	ax.autoscale_view()

	for i in flag:
	    h = i[2]
	    d = i[0]
	    l = i[3]
	    name = i[5]
	    att = i[6]
	    if(att == 'top'):
	        ax.annotate('', xy=(d, h), xytext=(d, h + 0.05),
	                    arrowprops=dict(facecolor='blue', width=0.5, shrink=0.25))
	    else:
	        ax.annotate('', xy=(d, l), xytext=(d, l - 0.05),
	                    arrowprops=dict(facecolor='green', width=0.5, shrink=0.25))
	# NOT WORKING


	plt.show()
