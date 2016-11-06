from result_insert import insert
from ..data_level import mysql as mysql
from multiprocessing.dummy import Pool
from multiprocessing import Process
from getdata import getdata
import time
from ..data_level import multprocess_stock as pl
#from getdata import getdata


class get_indexdata(object):
    """docstring for getdata"""

    def __init__(self, code='600123'):
        pl.get_index_data(code)
        self.pl = 1


class update_data(getdata):
    """docstring for update_data"""

    def __init__(self, code):
        getdata.__init__(self, code)
        #self.arg = arg


class run(insert):
    """docstring for run"""

    def __init__(self, code):
        insert.__init__(self, code)
        # print code
        # time.sleep(0.1)
        self.run()


class multi_run(run, update_data):
    """docstring for multi_run"""

    def __init__(self):
        self.codes = mysql.select_code_name().code.tolist()
        self.index = ['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb']

    def _run(self):
        lim = 1000
        for i in xrange(0, len(self.codes), lim):
            print i, i + lim
            p = Process(target=self.pool_fun_run,
                        args=[self.codes[i:i + lim], ])
            p.start()
            # p.join()
            time.sleep(0.5)
        # p1 = Process(target=self.pool_fun,args=[self.codes[0:1000],])
        # p1.start()
        # p2 = Process(target=self.pool_fun,args=[self.codes[1000:2000],])
        # p2.start()
        # p3 = Process(target=self.pool_fun,args=[self.codes[2000:],])
        # p3.start()
        # return p

    def _update(self):
        lim = 1000
        for i in xrange(0, len(self.codes), lim):
            print i, i + lim
            p = Process(target=self.pool_fun_update,
                        args=[self.codes[i:i + lim], ])
            p.start()
            p.join()
            time.sleep(0.1)

    def _update_index(self):
        for i in self.index:
            print i
            get_indexdata(i)

    def pool_fun_run(self, codes):
        pool = Pool(60)
        pool.map(run, codes)
        # pool.close()
        # pool.join()

    def pool_fun_update(self, codes):
        pool = Pool(60)
        pool.map(update_data, codes)


"calculate the new data and insert"
# test._run()
# test._update()
