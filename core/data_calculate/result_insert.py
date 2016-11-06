from ..data_level import mysql as mysql
from zen_data_result import zen_trend
from pandas.util.testing import assert_frame_equal
#import time
class insert(zen_trend):
	"""docstring for insert"""
	def __init__(self, code):
		zen_trend.__init__(self,code)
		self.old_top_bottom_return=mysql.select_without_index(table='test_table',code=self.code).sort_index()
		#time.sleep(0.05)
		self.old_trend_return=mysql.select_trend(code=self.code).sort_index()
		#time.sleep(0.05)
		self.old_rough_trend_return=mysql.select_trend(table='stock_trend_calculate',code=self.code).sort_index()
		#time.sleep(0.05)

	"""there are some problem"""
	def compare(self,df_old,df):
		# if 'index' in df.columns:
		# 	df['index']=df['index'].astype('int')
		# 	df['duration']=df['duration'].astype('int')
		#  	print 'reindex'
		#  	df=df.set_index('index')
		if df.index[-1]==df_old.index[-1]:
			return True
		else:
			return self.filter(df_old,df)

		try:
		    assert_frame_equal(df_old,df)
		    #self.insert = self.filter(self.old_top_bottom_return, self.top_bottom_return)
		    print 'eq'
		    return True
		except:  # appeantly AssertionError doesn't catch all
			
			assert_frame_equal(df_old,df)
			return self.filter(df_old,df)
			#return False

	def filter(self,df_old,df):
		begin=df_old.index[-1]+1
		end=df.index[-1]
		#print begin,end
		return df.ix[begin:end]

	def update(self,df_old,df,table):
		check=self.compare(df_old,df)
		if(type(check)!=bool):
			mysql.insert_tab(check,table)
			print self.code,table,'insert'
		else:
			print self.code,table,'already done'

	def run(self):
		#mysql.insert_tab(self.insert,'test_table')
		self.update(self.old_top_bottom_return,self.top_bottom_return,'test_table')
		#time.sleep(0.05)
		self.update(self.old_trend_return,self.trend_return,'stock_trend')
		#time.sleep(0.05)
		self.update(self.old_rough_trend_return,self.rough_trend_return,'stock_trend_calculate')
		#time.sleep(0.05)
		#mysql.insert_tab(self.trend_return,'stock_trend')
		#mysql.insert_tab(self.rough_trend_return,'stock_trend_calculate')

		
		
#code_629=insert('002269')
#code_123=insert('600123')