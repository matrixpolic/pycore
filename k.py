import core.data_level.mysql as mysql

df = mysql.select_basd_on_code('600123')


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



k_list = []
for i in range(0, df.open.count()):
    k_list.append(k(df.ix[i]))


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

filter_k = []
for i in range(0, len(k_list)):
    if(len(filter_k) == 0):
        filter_k.append(k_list[i])
    else:
        # campare and combine
        if(contain(filter_k[-1], k_list[i]) == "no_contain"):
            filter_k.append(k_list[i])
        else:

            if contain(filter_k[-1], k_list[i]) == "right_contain":
            	#print "r"
                if(len(filter_k) >= 2):
                    if filter_k[-1].top > filter_k[-2].top:
                        # top top
                        filter_k[-1]=contain_k(filter_k[-1],k_list[i],"tt","r")
                        pass
                    elif filter_k[-1].bottom < filter_k[-2].bottom:
                        # bottom bottom
                        filter_k[-1]=contain_k(filter_k[-1],k_list[i],"bb","r")
                        pass
            elif contain(filter_k[-1], k_list[i]) == "left_contain":
            	#print 'l'
            	if(len(filter_k) >= 2):
                    if filter_k[-1].top > filter_k[-2].top:
                    	#top top
                    	filter_k[-1]=contain_k(filter_k[-1],k_list[i],"tt","l")
                    	pass
                    elif filter_k[-1].bottom < filter_k[-2].bottom:
                    	#bottom bottom
                    	filter_k[-1]=contain_k(filter_k[-1],k_list[i],"bb","l")
                    	pass
        pass

for i in range(0,len(filter_k)):
	if(i>=2):
		contain_check(filter_k[i-1], filter_k[i])











