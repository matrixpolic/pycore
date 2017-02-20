
class k(object):
    """docstring for ClassName"""

    def __init__(self, arg):
        self.k = arg
        self.__arg = arg
        self.__attri_k_cal()

    def __attri_k_cal(self):
        if(self.__arg.close > self.__arg.open):
            self.attri_k = "rise"
            self.column_top = self.__arg.close
            self.column_bottom = self.__arg.open

        elif(self.__arg.close < self.__arg.open):
            self.attri_k = "fale"
            self.column_top = self.__arg.open
            self.column_bottom = self.__arg.close
        else:
            self.attri_k = "eq"

        self.top = self.__arg.high
        self.bottom = self.__arg.low


class contain_k(object):

    def __init__(self, pre_k, k, trend, c_type):
    	self.k_list = []
        self.k = k
        self.pre_k = pre_k
        self.trend = trend
        self.c_type=c_type
        if(self.c_type=="r"):
        	self.r_combine()
        elif(self.c_type=="l"):
        	self.l_combine()

    def r_combine(self):
    	if isinstance(self.pre_k, contain_k):
    		self.k_list = self.pre_k.k_list
    		self.k_list.append(self.k)
    		if(self.trend == "tt"):
    			self.top = self.k.top
    			self.bottom = self.pre_k.bottom
    		elif(self.trend == "bb"):
    			self.top = self.pre_k.top
    			self.bottom = self.k.bottom
    		pass
    	else:
    		self.k_list.append(self.pre_k)
    		self.k_list.append(self.k)
    		if(self.trend == "tt"):
    			self.top = self.k.top
    			self.bottom = self.pre_k.bottom
    		if(self.trend == "bb"):
    			self.top = self.pre_k.top
    			self.bottom = self.k.bottom
    		pass

    def l_combine(self):
    	if isinstance(self.pre_k, contain_k):
    		self.k_list = self.pre_k.k_list
    		self.k_list.append(self.k)
    		if(self.trend == "tt"):
    			self.top = self.pre_k.top
    			self.bottom = self.k.bottom
    		elif(self.trend == "bb"):
    			self.top=self.k.top
    			self.bottom=self.pre_k.bottom
    		pass
    	else:
    		self.k_list.append(self.pre_k)
    		self.k_list.append(self.k)
    		if(self.trend == "tt"):
    			self.top = self.pre_k.top
    			self.bottom = self.k.bottom
    		elif(self.trend == "bb"):
    			self.top=self.k.top
    			self.bottom=self.pre_k.bottom
    		pass

class sub_contain_k(contain_k):
	"""docstring for sub_combin_k"""
	def __init__(self, pre_k, k, trend, c_type):
		contain_k.__init__(self,pre_k, k, trend, c_type)
		self.getK()

	def getTop(self,test):
		k_top=[]
		for i in test:
			k_top.append(i.top)
		return k_top.index(max(k_top))

	def getBottom(self,test):
		k_bottom=[]
		for i in test:
			k_bottom.append(i.bottom)
		return k_bottom.index(min(k_bottom)) 
		
	def getK(self):
		self.top_k=self.k_list[self.getTop(self.k_list)]
		self.bottom_k=self.k_list[self.getBottom(self.k_list)]

		pass	




def contain(pre_k, k):
    if(pre_k.top >= k.top and pre_k.bottom <= k.bottom):
        return "left_contain"
    elif(pre_k.top <= k.top and pre_k.bottom >= k.bottom):
        return "right_contain"
    else:
        return "no_contain"

    pass
# check if still have contain status


def contain_check(pre_k, k):
    if(pre_k.top >= k.top and pre_k.bottom <= k.bottom):
        print "left contain"
    elif(pre_k.top <= k.top and pre_k.bottom >= k.bottom):
        print "right contain"
    else:
        print "no contain"

    pass



#insert to db
# mysql.insert_tab(cat_model, code)



	











