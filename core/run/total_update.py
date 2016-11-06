from ..data_calculate.multi_run import multi_run
from ..data_calculate.multi_calculate import myThread
from ..data_level import mysql as mysql
import time
import datetime
def run():
	#today = datetime.datetime.now().strftime('%Y-%m-%d')
	#end_date=mysql.select_index('sh').ix[-1].name

	#if(datetime.datetime.now().isoweekday()==6 or datetime.datetime.now().isoweekday()==7):
		print "67"

	 	run=multi_run()

	# 	"update original data"
	 	run._update_index()
	 	run._update()

	#codes = mysql.select().code.tolist()
	#codes = mysql.select_code_name().code.tolist()
	#end_date = datetime.datetime.now().strftime('%Y-%m-%d')
	#end_date="2016-04-08"
	#end_date=mysql.select_index('sh').ix[-1].name
	#end_date='2016-03-31'
	#already_codes = mysql.select_day_mark(end_date).code.tolist()
	#result = [i for i in codes if i not in already_codes]

		time.sleep(5)
	#thread = myThread(result, 2)
	#thread.process()