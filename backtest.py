import core.data_level.mysql as mysql
import pandas as pd
from k import contain_k, k, contain, contain_check, sub_contain_k
from strategy import filter_k_list
from strategy_func import only_top_bottom





def get_k_list(df):
    for i in range(0, df.open.count()):
        yield k(df.ix[i])

def backtest(sig ,account):
    money = account[0]
    num = account[1]
    stock = num*100

    #num =3
    if sig is not None:
        if(sig.has_key("buy")):
            if stock == 0:
                price = sig["buy"]
                num=int(money/3/price/100)
                
                if(money > price * num*100):
                    money = float(money) - price * num*100
                    stock = num*100
                    print "num:",num
                    print "------buy-----------"
               	    print "money:", float(money)
                    print "stock:", stock
                    print "---------------------"
                    account=[money,num]
                else:
                    print "money not enough"

                
            else:
                print "already buy stock,can not trade"
        else:
            if(stock != 0):
                price = sig["sell"]
                money = float(money) + num * price*100
                stock = 0
                num=0
                print "------sell-----------"
                print "money:", float(money)
                print "stock:", stock
                print "---------------------"
                account=[money,num]
            else:
                print "no stock,can not sell"
    	return account
    else:
    	print "no sig"
    	return account


code = "000009"
df = mysql.select_basd_on_code(code)


old_len = 0

k_list = []
cat_model = pd.DataFrame([], columns=['code', 'date', 'type'])

account=[10000,0]
for i in get_k_list(df):
    k_list.append(i)
    filter_k = filter_k_list([], k_list)
    if(len(filter_k) > old_len):
        old_len = len(filter_k)
        if(len(filter_k) >= 3):
            sig = only_top_bottom(filter_k[-3:], cat_model)
            account=backtest(sig,account)
            print account
