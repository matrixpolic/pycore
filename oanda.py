# coding:utf-8
import core.data_level.mysql as mysql
# import requests
# import json
import pandas as pd
#granularity=M5--> 5mini bar 
#S5->5 second
#count=10 --->get 10 rows data
#candleFormate=midpoint

#Asia/Shanghai
#获取数据库中的时间
def insert_result_to_db(result,df,table='GBP_USD'):
	
	data_dic=result.json();
	instrument=data_dic['instrument']
	candles=data_dic['candles']
	# granularity=data_dic['granularity']
	pd_data = pd.DataFrame(columns=("code", "type", "open", "high", "close",
	                                    "low", "date"))
	pd_data_ma6 = pd.DataFrame(columns=("code", "type", "open", "high", "close",
	                                    "low", "date","ma5"))
	test=[]
	# close=[]

	if(df.empty==False):
		for i in df[-6:-1].iterrows():
			row=i[1]
			test.append([row['code'],row['type'],row['open'],row['high'],row['close'],row['low'],row['date']])


	for i in candles:
		test.append([instrument,i['complete'],i['openMid'],i['highMid'],i['closeMid'],i['lowMid'],i['time']])
		#Ndetail.loc[i]
		# close.append(i['closeMid'])
		# if(len(close)>=6):
		# 	print close[-6:].mean()

	for i in xrange(0,len(test)):
		pd_data.loc[i]=test[i]
		if(pd_data.count().close>=6 and pd_data.loc[i].type==1):
			# print i,pd_data.close[-6:].mean()
			test[i].append(pd_data.close[-6:].mean())
			pd_data_ma6.loc[i]=test[i]

	pd_data_ma6=pd_data_ma6.drop(pd_data_ma6.iloc[0].name)
	print pd_data_ma6
	if(pd_data_ma6.empty==False):
	# for i in xrange(0,len(test),3):
	# 	print i
		mysql.insert_tab(pd_data_ma6, table)
	else:
		print "empty"
		return "empty";

def getUrl(instrument,granularity,df):
	
	# df=df.sort("date")
	if(df.empty==False):
		time=df.iloc[-1].date.to_datetime()
		# time.strptime("Y-m-d");

		start_str=time.strftime("%Y-%m-%dT%H:%M:%SZ").replace(":","%3A");
		# condition="instrument=GBP_AUD&granularity=M5&count=10&candleFormat=midpoint"
		# granularity=granularity
		url = "https://api-fxpractice.oanda.com/v1/candles?instrument="+instrument+"&candleFormat=midpoint&granularity="+granularity+"&count=200&start="+start_str
	else:
		granularity="M5"
		url = "https://api-fxpractice.oanda.com/v1/candles?instrument="+instrument+"&candleFormat=midpoint&granularity="+granularity+"&count=200"
	return url
#url = "https://api-fxpractice.oanda.com/v1/prices?instruments=EUR_USD"
