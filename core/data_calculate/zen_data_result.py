from stock_data_analysis_mod import data_analysis
import pandas as pd


class zen_trend(data_analysis):
	"""docstring for zen_trend"""
	def __init__(self, code='600123'):
		data_analysis.__init__(self,code)
		self.trend_source=self.mark_result_filter_test()

		self.top_bottom_return=self.top_bottom()
		self.trend_return=self.trend()
		self.rough_trend_return=self.rough_trend()
	
	def top_bottom(self):
	    l = self.mark_result()
	    df = pd.DataFrame(columns=('date', 'key', 'code'))
	    for i in xrange(0, len(l)):
	        value = l[i][0]
	        key = l[i][0].keys()[0]
	        detail = value[key]
	        # print
	        # key,detail.name,detail.open,detail.high,detail.low,detail.close,'600123'
	        df.loc[i] = [detail.name, key, self.code]
	    #mysql.insert_tab(df, 'test_table')
	    #self.top_bottom=df
	    return df

	def trend(self):
    # l=total_cal(code)
	    source = self.trend_source
	    data = self.df
	    df = pd.DataFrame(columns=('key', 'begin', 'end',
	                               'index', 'duration', 'code'))
	    # for x in l:
	    # 	key=x.keys()[0]
	    # 	lis=x[x.keys()[0]]
	    # 	print key,lis

	    for x in xrange(0, len(source)):
	        s_key = source[x].keys()[0]
	        value = source[x][s_key]
	        begin = value[0]
	        end = value[1]
	        duration = -data.index.tolist().index(begin.name) + \
	            data.index.tolist().index(end.name)
	        #print s_key, begin.name, end.name, code, x, duration
	        df.loc[x] = [s_key, begin.name, end.name, int(x), duration, self.code]
	   
	    return df


	def rough_trend(self):
	    l = self.total_cal_return
	    df = pd.DataFrame(columns=('key', 'rel_index', 'code', 'num', 'index'))
	    for x in xrange(0, len(l)):
	        # print [l[x].keys()[0], str(l[x][l[x].keys()[0]])[1:-1],
	        #        code, len(l[x][l[x].keys()[0]]), x]
	        df.loc[x] = [l[x].keys()[0], str(l[x][l[x].keys()[0]])[1:-1],
	                     self.code, len(l[x][l[x].keys()[0]]), int(x)]
	    
	    return df


#test=zen_trend()