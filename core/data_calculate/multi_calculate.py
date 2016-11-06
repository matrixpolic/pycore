from ..data_level import mysql as mysql
from multiprocessing.dummy import Pool
import threading
import time
from time import sleep, ctime
from multiprocessing import Process
from getdata import getdetail
import sys
import datetime
import pandas as pd



class run(getdetail):
    """docstring for run"""

    def __init__(self, code):
        end_date=mysql.select_index('sh').ix[-1].name
        self.df = mysql.select_index(code)[-120:]
        date=self.df.iloc[-1].name
        if date==end_date:
            getdetail.__init__(self, code)
            self.init_mark=1
        else:
            print code,'this stock stop trading today'
            self.init_mark=0
        # print code
        # time.sleep(0.1)
       

   


class myThread ():
    """docstring for myThread"""

    def __init__(self, codes, nsec):
        #super(myThread, self).__init__()
        self.codes = codes
        self.nsec = nsec
        self.df = []
        self.trend_return=[]
        self.threads()

    def run(self, code):
        print 'start code', code, 'at:', ctime()
        instance=run(code)
        if(instance.init_mark==1):
            print instance.coordinate()
            
            self.df.append(instance.coordinate())
            if instance.flag ==1:
                print instance.insert_trend_return
                self.trend_return.append(instance.insert_trend_return)
        # sleep(self.nsec)
        print 'code', code, 'done at:', ctime()

    def threads(self):
        self.thread = []
        for i in self.codes:
            t = threading.Thread(target=self.run, args=(i,))
            self.thread.append(t)

    def start(self, inp):
        lis = inp
        lim = 30
        for i in xrange(0, len(lis), lim):
            print i, i + lim
            for x in lis[i:i + lim]:
                # print i,i+lim
                # pass
                x.start()
    # sleep(0.5)
            for x in lis[i:i + lim]:
                x.join()
                # pass
            print '----now-----', i + lim
            print '----left-----', len(lis) - i - lim
    # print i,i+lim
        # print self.df
        # print len(self.df)
        df = pd.DataFrame(
            columns=('type', 'date', 'code', 'mark_low', 'mark_high'))
        for i in xrange(0, len(self.df)):
            df.loc[i] = self.df[i]
        print df
        #print self.trend_return
        mysql.insert_tab(df,'day_mark')
        if self.trend_return:
            result=pd.concat(self.trend_return)
            mysql.insert_tab(result,'stock_trend')
            print result
        
        

       

    def process(self):
        lim = 600
        lis = self.thread
        p = []
        for i in xrange(0, len(lis), lim):
            print i, i + lim
            p.append(Process(target=self.start, args=[lis[i:i + 600], ]))

            # sleep(1)
        for x in p:
            x.start()
            sleep(1)

        for x in p:
            x.join()

        print 'all done'
        #sys.exit('all process quite')


#test = myThread(result, 2)
#test.process()
#test.threads()
#test.start(test.thread)
#test.run('600123')
