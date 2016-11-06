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
                    'rise_begin': i, 'pre_fall_duration': self.false_count_total, "rise days": self.true_count, "index": i, "type": "rise_begin"}
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
                    'fall_begin': i, 'pre_rise_duration': self.true_count_total, "fall days": self.false_count, "index": i, "type": "fall_begin"}
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


class getN():
    """docstring for getN"""

    def __init__(self, df):
        self.pre_N = []
        self.dic_key_point = []
        self.df = df

    def N_struct_obo(self, dic):
        if(len(dic.keys()) >= 4):
            self.dic_key_point.append(dic)

            # key_index=dic['index']-1
            #price = self.df.ix[key_index].ma5
            # print key_index+1,dic['type'],price
            if(len(self.dic_key_point) >= 4):
                self.four_price_count()

        pass

    def four_price_count(self):
        rise_or_fall_N = self.dic_key_point[-4:]
        n4 = rise_or_fall_N[3]
        n3 = rise_or_fall_N[2]
        n2 = rise_or_fall_N[1]
        n1 = rise_or_fall_N[0]
        n4_price = self.df.ix[n4['index'] - 1].ma5
        n3_price = self.df.ix[n3['index'] - 1].ma5
        n2_price = self.df.ix[n2['index'] - 1].ma5
        n1_price = self.df.ix[n1['index'] - 1].ma5
        if (n4_price > n3_price)and (n2_price > n1_price) and (n4_price > n2_price):
            if(n3_price > n1_price):
                # print "standard rise
                # N",n1['index'],n2['index'],n3['index'],n4['index']
                self.pre_N.append(
                    {"standard_rise_n": rise_or_fall_N, "type": "standard_rise_n"})
            else:
                # print "---check---rise
                # N",n1['index'],n2['index'],n3['index'],n4['index']
                self.pre_N.append(
                    {"unst_rise_n": rise_or_fall_N, "type": "unst_rise_n"})
                # print n1_price,n2_price,n3_price,n4_price
                # print self.rise_N
                # self.N.append({"rise_N":self.rise_N})
                #self.rise_N = []
        if (n1_price > n2_price) and (n3_price > n4_price) and (n2_price > n4_price):
            if(n1_price > n3_price):
                # print "standard fall
                # N",n1['index'],n2['index'],n3['index'],n4['index']
                self.pre_N.append(
                    {"standard_fall_n": rise_or_fall_N, "type": "standard_fall_n"})
            else:
                # print "---check---fall
                # N",n1['index'],n2['index'],n3['index'],n4['index']
                self.pre_N.append(
                    {"unst_fall_n": rise_or_fall_N, "type": "unst_fall_n"})
        pass


class analysisN():
    """docstring for analysisN"""

    def __init__(self,df):
        self.df = df
        self.mark = 0
        self.preN=None
        self.buy=[]
        self.sell=[]
        self.dic =[]
        self.all_n=[]
    #get standard n
    def pickN(self,pre_N):
        if len(pre_N) >self.mark:
            self.preN = pre_N
            N=pre_N[-1]
            result=self.N_detail(N)
            print result['n1_index'],result['n2_index'],result['n3_index'],result['n4_index']
            print result['state'],result['n1_price'],result['n2_price'],result['n3_price'],result['n4_price']
            if result['state']=="standard_fall_n":
                self.buy.append(result['n4_index'])
                self.dic.append(N)
                #print result['n4_index']
            elif result['state']=="standard_rise_n":
                self.dic.append(N)
                self.sell.append(result['n4_index'])
            self.mark += 1
        pass
    #get all n
    def pic_all_N(self,pre_N):
        if len(pre_N) >self.mark:
            self.preN = pre_N
            N=pre_N[-1]
            result=self.N_detail(N)
            print result['n1_index'],result['n2_index'],result['n3_index'],result['n4_index']
            print result['state'],result['n1_price'],result['n2_price'],result['n3_price'],result['n4_price']
            self.all_n.append(N)
            self.mark += 1
        pass
    def N_detail(self,N):
        state=N['type']
        detail=N[state]
        n4 = detail[3]
        n3 = detail[2]
        n2 = detail[1]
        n1 = detail[0]
        n4_price = self.df.ix[n4['index'] - 1].ma5
        n3_price = self.df.ix[n3['index'] - 1].ma5
        n2_price = self.df.ix[n2['index'] - 1].ma5
        n1_price = self.df.ix[n1['index'] - 1].ma5
        result = {
            "state":state,
            "n1_price":n1_price,
            "n2_price":n2_price,
            "n3_price":n3_price,
            "n4_price":n4_price,
            "n1_index":n1['index']-1,
            "n2_index":n2['index']-1,
            "n3_index":n3['index']-1,
            "n4_index":n4['index']-1


        }
        return result












































