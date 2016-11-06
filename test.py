import core.data_level.mysql as mysql
from core.data_calculate.multi_run import multi_run
import core.data_level.multprocess_stock as multp_stock
from core.data_calculate.zen_data_result import zen_trend
from core.data_calculate.stock_data_analysis_mod import data_analysis
#info = mysql.select_code_name()
# print mysql.select_code_name().code.tolist()
nums = mysql.select().code.tolist()
code = mysql.select_code_name().code.tolist()
result=[i for i in code if i not in nums]


		

class data_analysis_test(data_analysis,zen_trend):
    """docstring for test"""
    def __init__(self, code,days=5):
        
        self.days=days
        #super(data_analysis, self).__init__()
        self.df = mysql.select_index(code)
        self.code = code
        self.test = self.stock_ana_test()
        self.mark_result_return = self.mark_result()
        self.total_cal_return = self.total_cal()
        self.trend_source=self.mark_result_filter_test()


    def mark_result_filter_test(self):
    	days=self.days
        l = self.mark_result_return
        df = self.df
        lim = len(l) - 1
        #print l
        #return 1
        #print lim
        result = list()
        for x in xrange(0, lim):
            mark = l[x][0].keys()[0]
            mark_value = l[x][0].values()[0].name
            mark_value_price = l[x][0].values()[0]
            next_mark = l[x + 1][0].keys()[0]
            next_mark_value = l[x + 1][0].values()[0].name
            next_mark_value_price = l[x + 1][0].values()[0]

            if(mark == 'top' and next_mark == 'bottom'):
                dur = -df.index.tolist().index(mark_value) + \
                    df.index.tolist().index(next_mark_value)

                # result.append(l[x])
                if(dur >= days):
                    # print mark_value,mark_value_price.open,'--fall--',next_mark_value,next_mark_value_price.close,dur
                    # print mark_value_price,next_mark_value_price
                    result.append(
                        {'fall': [mark_value_price, next_mark_value_price]})
                    # result.append(l[x])
                    # result.append(l[x+1])
                # pass
            if(mark == 'bottom' and next_mark == 'top'):
                dur = -df.index.tolist().index(mark_value) + \
                    df.index.tolist().index(next_mark_value)
                # result.append(l[x])
                if(dur >= days):
                    # print mark_value,mark_value_price.close,'--rise--',next_mark_value,next_mark_value_price.open,dur
                    # print mark_value_price,next_mark_value_price
                    result.append(
                        {'rise': [mark_value_price, next_mark_value_price]})
                    # result.append(l[x])
                    # result.append(l[x+1])
        return result
    def total_cal(self):
        l = self.filter_result()
        fall = []
        rise = []
        total = []
        #print l
        #return 1
        for x in l[0]:
            if x['fall'] != []:
                fall.append(x)
        for x in l[1]:
            if x['rise'] != []:
                rise.append(x)
        if rise[0]['rise'][0] == 0:
            for r in rise:
                for f in fall:
                    rise_end = r['rise'][-1] + 1
                    fall_beg = f['fall'][0]
                    if(rise_end == fall_beg):
                        total.append(r)
                        total.append(f)

            if len(total) != len(rise) + len(fall):
                for x in rise[rise.index(rise[-2]) + 1:len(rise)]:
                    total.append(x)

        elif(fall[0]['fall'][0] == 0):
            for f in fall:
                for r in rise:
                    fall_beg = f['fall'][-1] + 1
                    rise_end = r['rise'][0]

                    if(rise_end == fall_beg):
                        total.append(f)
                        total.append(r)

            if len(total) != len(rise) + len(fall):
                # print 'wrong fall',fall[fall.index(fall[-2])+1:len(fall)]
                for x in fall[fall.index(fall[-2]) + 1:len(fall)]:
                    total.append(x)

        return total

    

    
class insert_new_stock(data_analysis_test,zen_trend):
	"""docstring for insert_new_stoc"""
	def __init__(self, code,days):
		data_analysis_test.__init__(self,code,days)
		self.trend_source=self.mark_result_filter_test()

		self.top_bottom_return=self.top_bottom()
		self.trend_return=self.trend()
		self.rough_trend_return=self.rough_trend()
		#zen_trend.__init__(self, code)
	def update(sefl,df,table):
		mysql.insert_tab(df,table)
		pass

	def run(self):
		#mysql.insert_tab(self.insert,'test_table')
		self.update(self.top_bottom_return,'test_table')
		#time.sleep(0.05)
		self.update(self.trend_return,'stock_trend')
		#time.sleep(0.05)
		self.update(self.rough_trend_return,'stock_trend_calculate')
		

def test():
	for i in result[47:]:
		try:
			a=insert_new_stock(i)
			a.run()
		except Exception, e:
			print i
			a=insert_new_stock(i,1)
			a.run()
			pass
		finally:
			pass

		
	#return a
# for i in result[1:]:
# 	multp_stock.get_hist_data(i)
#print result
#test();
#a=insert_new_stock('002792',1)
b=data_analysis_test('002792',1)



