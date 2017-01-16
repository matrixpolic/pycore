from getGBPdata import getGBPdata
from calculate_n_struct_and_insert_into_db import total_run

import core.data_level.mysql as mysql
import pandas as pd

from sys import argv,exit

instrument="GBP_USD"
#get argment from cmd
arg=argv

def numbers_to_list(argument):
    switcher = {
        '5': ["GBP_USD","M5","GBP_USE_N_struct"],
        #'30': ["GBP_USD30","M30","GBP_USE_N_struct30"],
        '5XAU': ["XAU_USD","M5","XAU_USD_N_struct"],
        '5EUR': ["EUR_USD","M5","EUR_USD_N_struct"],
        '5JPY': ["USD_JPY","M5","USD_JPY_N_struct"],
       
    }
    return switcher.get(argument, "nothing")

if(len(arg)>=2):
	# print arg
	info_list=numbers_to_list(arg[1])
	if(info_list=="nothing"):
		print "****************"
		print "*somthing wrong*"
		print "*arg only 5,30 *"
		print "****************"
		exit();

	table=info_list[0]
	granularity=info_list[1]
	n_table=info_list[2]
	instrument=table

	if getGBPdata(instrument, table, granularity) !="empty":	
		df=mysql.select_with_index(table,instrument);
		# old_df=mysql.select_without_index(n_table,instrument," ")
		result=total_run(df, instrument,table,n_table)
