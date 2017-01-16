from apscheduler.schedulers.blocking import BlockingScheduler
import core.data_level.mysql as mysql
from getGBPdata import getGBPdata
from calculate_n_struct_and_insert_into_db import total_run

def m5():
	instrument="GBP_USD"
	info_list=["GBP_USD","M5","GBP_USE_N_struct"]
	table=info_list[0]
	granularity=info_list[1]
	n_table=info_list[2]
	if getGBPdata(instrument, table, granularity) !="empty":	
		df=mysql.select_with_index(table,instrument);
		# old_df=mysql.select_without_index(n_table,instrument," ")
		result=total_run(df, instrument,table,n_table)
	return result

def m30():
	instrument="GBP_USD"
	info_list=["GBP_USD30","M30","GBP_USE_N_struct30"]
	table=info_list[0]
	granularity=info_list[1]
	n_table=info_list[2]
	if getGBPdata(instrument, table, granularity) !="empty":	
		df=mysql.select_with_index(table,instrument);
		# old_df=mysql.select_without_index(n_table,instrument," ")
		result=total_run(df, instrument,table,n_table)
	return result


#must define the UTC
sched = BlockingScheduler(timezone="UTC")
sched.add_job(m5, 'interval', hours=1)
sched.add_job(m30, 'interval', hours=6)
sched.start()
