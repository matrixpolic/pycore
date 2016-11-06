from ..database.mysql.mysql_db import MySqlDb
from ..data_level import mysql as mysql
from ..data_calculate.stock_data_analysis_mod import data_analysis
from ..data_calculate.multi_calculate import run
# test mysql db
class MySqlDbTest:
    def __init__(self):
        db = MySqlDb()
        self.result = "Module: " + db.name
        self.test=run('600123')
        #print mysql.select_index('sh')