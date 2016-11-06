# coding:utf-8
from oanda import getUrl,insert_result_to_db
import core.data_level.mysql as mysql
import requests
import json
import pandas as pd

headers = {	'Authorization': '101-004-4052008-001 2e4fbc4ab3d4fb9c8bc5050d14409d97-5aa9c73f1b01fa84afc3f77615efacdb',
            'X-Target-URI': 'https://api-fxpractice.oanda.com',
            'Connection': 'Keep-Alive',
            'Host': 'api-fxpractice.oanda.com'
            }

# instrument="GBP_USD"


# table="GBP_USD30"
# granularity="M30"

# table="GBP_USD"
# granularity="M5"
def getGBPdata(instrument,table,granularity):
	df=mysql.select_without_index(table,instrument);
	url=getUrl(instrument,granularity,df)
	print url
	rs = requests
	# result = rs.get(url,headers=headers)
	result = rs.get(url)
	# data=json.dumps(result.json());
	print result

	insert_result_to_db(result,df,table)


