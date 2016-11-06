import core.data_level.mysql as mysql

df = mysql.select_basd_on_code('600123')

# for i in df.iterrows():
# 	print i[1]['ma5']


class count():
    """docstring for resovel"""

    def __init__(self, df):
        self.df = df
        self.false_count = 0
        self.true_count = 0
        self.true_count_total = 0
        self.false_count_total = 0
        self.mark = None
        self.pre_mark = None
        self.rise_begin_dic = None
        self.fall_begin_dic = None
        self.list = []

    def top_down_resovle(self, price, pre_price):
        if(price >= pre_price):
            # print "total_false_count:%d", self.false_count
            self.mark = 'rise'

            # print "true:%d", self.true_count
        else:
            # print "total_true_count:%d",self.true_count
            self.mark = 'fall'

            # print "false_count:%d", self.false_count

    def trace(self, i):

        if self.mark == 'rise':
            self.false_count_total = self.false_count
            if(self.false_count != 0):
                # print {'rise_begin': i, 'pre_fall_duration:':
                # self.false_count_total}
                self.true_count += 1
                self.rise_begin_dic = {
                    'rise_begin': i, 'pre_fall_duration': self.false_count_total, "rise days": self.true_count, "index": i,"type":"rise_begin"}
                self.list.append(self.rise_begin_dic)
                self.false_count = 0

            else:

                # self.rise_begin_dic=None

                self.true_count += 1
                # print i,"rise days:",self.true_count
                self.list.append({"index": i, "rise days": self.true_count})

        if self.mark == 'fall':
            # self.true_count = 0
            self.true_count_total = self.true_count
            if(self.true_count != 0):
                # print {'fall_begin:': i, 'pre_rise_duration:':
                # self.true_count_total}
                self.false_count += 1
                self.fall_begin_dic = {
                    'fall_begin': i, 'pre_rise_duration': self.true_count_total, "fall days": self.false_count, "index": i,"type":"fall_begin"}
                self.list.append(self.fall_begin_dic)
                self.true_count = 0

            else:

                # self.fall_begin_dic=None
                self.false_count += 1
                # print i,"fall days:",self.false_count
                self.list.append({"index": i, "fall days": self.false_count})

    def run(self, i, price, pre_price):
        self.top_down_resovle(price, pre_price)
        self.trace(i)


class descision_tree():
    """docstring for descision_tree"""

    def __init__(self, df):
        self.df = df
        self.count = 0
        self.rise_N = []
        self.fall_N = []
        self.shock_N=[]
        self.N=[]
        self.pre_N=[]

    def analysis_N(self, dic):
        if(len(dic.keys()) >= 4):
            if dic.has_key('fall_begin'):
                print "fall begin index", dic['index'], "pre key index price is top point", self.df.ix[dic['index'] - 1].ma5
            else:
                print "rise begin index", dic['index'], "pre key index price is down point", self.df.ix[dic['index'] - 1].ma5
            self.count += 1
            if(self.count == 4):
                print "------", self.count, "-------"
                self.count = 0

    def N_rise_struct(self, dic):
        if(len(dic.keys()) >= 4):
            self.rise_N.append(dic)
            if(len(self.rise_N) == 4):
                n4 = self.rise_N[3]
                n3 = self.rise_N[2]
                n2 = self.rise_N[1]
                n1 = self.rise_N[0]
                n4_price = self.df.ix[n4['index'] - 1].ma5
                n3_price = self.df.ix[n3['index'] - 1].ma5
                n2_price = self.df.ix[n2['index'] - 1].ma5
                n1_price = self.df.ix[n1['index'] - 1].ma5

                if (n4_price > n3_price)and (n2_price > n1_price) and (n2_price > n3_price) and (n4_price>n1_price) and  (n4_price>n2_price) and (n3_price>n1_price):
                    #print "------stand rise N",n1['index'],n2['index'],n3['index'],n4['index']
                    #print n1_price,n2_price,n3_price,n4_price
                    #print self.rise_N
                    self.N.append({"rise_N":self.rise_N})
                    self.rise_N = []
                else:
                    self.rise_N.pop(0)

        pass
    def N_rise_struct_obo(self, dic):
        if(len(dic.keys()) >= 4):
            self.rise_N.append(dic)
            
            key_index=dic['index']-1
            price = df.ix[key_index].ma5
            print key_index+1,dic['type'],price
            if(len(self.rise_N)>=4):
            	self.four_price_count()

        pass
    def four_price_count(self):
    	rise_or_fall_N=self.rise_N[-4:]
        n4 = rise_or_fall_N[3]
        n3 = rise_or_fall_N[2]
        n2 = rise_or_fall_N[1]
        n1 = rise_or_fall_N[0]
        n4_price = self.df.ix[n4['index'] - 1].ma5
        n3_price = self.df.ix[n3['index'] - 1].ma5
        n2_price = self.df.ix[n2['index'] - 1].ma5
        n1_price = self.df.ix[n1['index'] - 1].ma5    
        if (n4_price > n3_price)and (n2_price > n1_price) and (n4_price>n2_price): 
        	if(n3_price>n1_price):
        		print "standard rise N",n1['index'],n2['index'],n3['index'],n4['index']
        		self.pre_N.append({"standard_rise_n":rise_or_fall_N,"type":"standard_rise_n"})
        	else:
        		print "---check---rise N",n1['index'],n2['index'],n3['index'],n4['index']
        		self.pre_N.append({"unst_rise_n":rise_or_fall_N,"type":"unst_rise_n"})
                    #print n1_price,n2_price,n3_price,n4_price
                    #print self.rise_N
                    #self.N.append({"rise_N":self.rise_N})
                    #self.rise_N = []
        if (n1_price>n2_price) and (n3_price>n4_price) and (n2_price>n4_price):
        	if(n1_price>n3_price):
        		print "standard fall N",n1['index'],n2['index'],n3['index'],n4['index']
        		self.pre_N.append({"standard_fall_n":rise_or_fall_N,"type":"standard_fall_n"})
        	else:
        		print "---check---fall N",n1['index'],n2['index'],n3['index'],n4['index']
        		self.pre_N.append({"unst_fall_n":rise_or_fall_N,"type":"unst_fall_n"})
    	pass
    def N_fall_struct(self,dic):
    	if(len(dic.keys()) >= 4):
            self.fall_N.append(dic)
            if(len(self.fall_N) == 4):
                n4 = self.fall_N[3]
                n3 = self.fall_N[2]
                n2 = self.fall_N[1]
                n1 = self.fall_N[0]
                n4_price = self.df.ix[n4['index'] - 1].ma5
                n3_price = self.df.ix[n3['index'] - 1].ma5
                n2_price = self.df.ix[n2['index'] - 1].ma5
                n1_price = self.df.ix[n1['index'] - 1].ma5

                if (n4_price < n3_price)and (n2_price <n1_price) and (n2_price < n3_price) and (n1_price>n3_price) and(n4_price<n2_price) and(n4_price<n1_price):
                    #print "------stand fall N",n1['index'],n2['index'],n3['index'],n4['index']
                    #print n1_price,n2_price,n3_price,n4_price
                    #print self.fall_N
                    self.N.append({"fall_N":self.fall_N})
                    self.fall_N = []
                else:
                    self.fall_N.pop(0)

    	pass
    def N_struct(self,dic):
    	if(len(dic.keys()) >= 4):
            self.shock_N.append(dic)
            if(len(self.fall_N) == 4):
                n4 = self.shock_N[3]
                n3 = self.shock_N[2]
                n2 = self.shock_N[1]
                n1 = self.shock_N[0]
                n4_price = self.df.ix[n4['index'] - 1].ma5
                n3_price = self.df.ix[n3['index'] - 1].ma5
                n2_price = self.df.ix[n2['index'] - 1].ma5
                n1_price = self.df.ix[n1['index'] - 1].ma5

                if (n4_price < n3_price)and (n2_price <n1_price) and (n2_price < n3_price) and (n1_price>n3_price) and (n4_price>n2_price) and (n4_price<n1_price):
                    print "----stand fall shock N",n1['index'],n2['index'],n3['index'],n4['index']
                    print n1_price,n2_price,n3_price,n4_price
                    self.shock_N = []
                elif(n4_price > n3_price)and (n2_price >n1_price) and (n2_price > n3_price) and (n1_price<n3_price) and (n4_price<n2_price) and (n4_price>n1_price):
                	print "----stand fall shock N",n1['index'],n2['index'],n3['index'],n4['index']
                	print n1_price,n2_price,n3_price,n4_price
                	self.shock_N = []
                elif(n4_price > n3_price)and (n2_price >n1_price) and (n2_price > n3_price) and (n1_price>n3_price) and (n4_price>n2_price) and (n4_price>n1_price):
                	print "----stand fall shock N",n1['index'],n2['index'],n3['index'],n4['index']
                	print n1_price,n2_price,n3_price,n4_price
                	self.shock_N = []
               	elif(n4_price < n3_price)and (n2_price < n1_price) and (n2_price < n3_price) and (n1_price<n3_price) and (n4_price<n2_price) and (n4_price<n1_price):
                	print "----stand fall shock N",n1['index'],n2['index'],n3['index'],n4['index']
                	print n1_price,n2_price,n3_price,n4_price
                	self.shock_N = []
                else:
                    self.shock_N.pop(0)

    	pass

  	


ma5_list = df.ma5.tolist()
lenght = len(ma5_list) -750


false_count = 0
true_count = 0

obj_count = count(df)
dt = descision_tree(df)
mark=0
for i in xrange(0, lenght):
    if i - 1 > 0:
        pre_price = ma5_list[i - 1]
        price = ma5_list[i]

        # obj_count.top_down_resovle(price, pre_price)
        # obj_count.trace(i)
        obj_count.run(i, price, pre_price)

        dic = obj_count.list[-1]
       	# print dic
       	dt.N_rise_struct_obo(dic)
        # dt.N_rise_struct(dic)
        # dt.N_fall_struct(dic)
        if len(dt.pre_N)>mark:
        	print dt.pre_N[-1]
        	mark+=1
        

























