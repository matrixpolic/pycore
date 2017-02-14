import core.data_level.mysql as mysql
code ="000009"
df = mysql.select_basd_on_code(code)


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

import pandas as pd
cat_model=pd.DataFrame([],columns=['code','date','type'])

def getTop(test):
	k_top=[]
	for i in test:
		k_top.append(i.top)
	return k_top.index(max(k_top))

def getBottom(test):
	k_bottom=[]
	for i in test:
		k_bottom.append(i.bottom)
	return k_bottom.index(min(k_bottom))

for i in range(0,len(filter_k)):
	if(i>=3):
		#contain_check(filter_k[i-1], filter_k[i])
		if(filter_k[i-2].top<filter_k[i-1].top >filter_k[i].top):
			if isinstance(filter_k[i-1],contain_k):
				print "top formate contain_k"
				if(filter_k[i-1].c_type=="l"):
					print filter_k[i-1].k_list[getTop(filter_k[i-1].k_list)].k.name
					date_top = filter_k[i-1].k_list[getTop(filter_k[i-1].k_list)].k.name
					#test max
					#test=filter_k[i-1].k_list

					cat_model.loc[i-1]=[code,date_top,"top"]

				elif(filter_k[i-1].c_type=="r"):
					print filter_k[i-1].k_list[getTop(filter_k[i-1].k_list)].k.name
					date_top = filter_k[i-1].k_list[getTop(filter_k[i-1].k_list)].k.name

					cat_model.loc[i-1]=[code,date_top,"top"]
			else:
				print "top formate"
				print filter_k[i-1].k.name

				cat_model.loc[i-1]=[code,filter_k[i-1].k.name,"top"]

		elif(filter_k[i-2].bottom>filter_k[i-1].bottom <filter_k[i].bottom):
			if isinstance(filter_k[i-1],contain_k):
				print "bottom formate contain_k"
				if(filter_k[i-1].c_type=="l"):
					print filter_k[i-1].k_list[getBottom(filter_k[i-1].k_list)].k.name
					bottom = filter_k[i-1].k_list[getBottom(filter_k[i-1].k_list)].k.name

					cat_model.loc[i-1]=[code,bottom,"bottom"]
				elif(filter_k[i-1].c_type=="r"):
					print filter_k[i-1].k_list[getBottom(filter_k[i-1].k_list)].k.name
					bottom = filter_k[i-1].k_list[getBottom(filter_k[i-1].k_list)].k.name

					cat_model.loc[i-1]=[code,bottom,"bottom"]
			else:
				print "bottom formate"
				print filter_k[i-1].k.name
				cat_model.loc[i-1]=[code,filter_k[i-1].k.name,"bottom"]



#insert to db
mysql.insert_tab(cat_model, code)



	











