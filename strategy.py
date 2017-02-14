from k import contain_k, k, contain, contain_check, sub_contain_k
import core.data_level.mysql as mysql
import pandas as pd


code = "000009"
df = mysql.select_basd_on_code(code)


def filter_k_list(filter_k, k_list):
    for i in range(0, len(k_list)):
        if(len(filter_k) == 0):
            filter_k.append(k_list[i])
        else:
            # campare and combine
            if(contain(filter_k[-1], k_list[i]) == "no_contain"):
                filter_k.append(k_list[i])
            else:

                if contain(filter_k[-1], k_list[i]) == "right_contain":
                    # print "r"
                    if(len(filter_k) >= 2):
                        if filter_k[-1].top > filter_k[-2].top:
                            # top top
                            filter_k[-1] = sub_contain_k(filter_k[-1],
                                                         k_list[i], "tt", "r")
                            pass
                        elif filter_k[-1].bottom < filter_k[-2].bottom:
                            # bottom bottom
                            filter_k[-1] = sub_contain_k(filter_k[-1],
                                                         k_list[i], "bb", "r")
                            pass
                elif contain(filter_k[-1], k_list[i]) == "left_contain":
                    # print 'l'
                    if(len(filter_k) >= 2):
                        if filter_k[-1].top > filter_k[-2].top:
                            # top top
                            filter_k[-1] = sub_contain_k(filter_k[-1],
                                                         k_list[i], "tt", "l")
                            pass
                        elif filter_k[-1].bottom < filter_k[-2].bottom:
                            # bottom bottom
                            filter_k[-1] = sub_contain_k(filter_k[-1],
                                                         k_list[i], "bb", "l")
                            pass
    return filter_k


def getTop(test):
    k_top = []
    for i in test:
        k_top.append(i.top)
    return k_top.index(max(k_top))


def getBottom(test):
    k_bottom = []
    for i in test:
        k_bottom.append(i.bottom)
    return k_bottom.index(min(k_bottom))


def tb_cal(filter_k, cat_model):
        #contain_check(filter_k[i-1], filter_k[i])
    i = -1
    if(filter_k[i - 2].top < filter_k[i - 1].top > filter_k[i].top):
        if isinstance(filter_k[i - 1], sub_contain_k):
            print "top formate sub_contain_k"
            if(filter_k[i - 1].c_type == "l"):
                print filter_k[i - 1].top_k.k.name
                date_top = filter_k[
                    i - 1].k_list[getTop(filter_k[i - 1].k_list)].k.name
                # test max
                # test=filter_k[i-1].k_list

                cat_model.loc[i - 1] = [code, date_top, "top"]

            elif(filter_k[i - 1].c_type == "r"):
                print filter_k[i - 1].top_k.k.name
                date_top = filter_k[
                    i - 1].k_list[getTop(filter_k[i - 1].k_list)].k.name

                cat_model.loc[i - 1] = [code, date_top, "top"]
        else:
            print "top formate"
            print filter_k[i - 1].k.name

            cat_model.loc[i - 1] = [code, filter_k[i - 1].k.name, "top"]

    elif(filter_k[i - 2].bottom > filter_k[i - 1].bottom < filter_k[i].bottom):
        if isinstance(filter_k[i - 1], sub_contain_k):
            print "bottom formate sub_contain_k"
            if(filter_k[i - 1].c_type == "l"):
                print filter_k[i - 1].bottom_k.k.name

                bottom = filter_k[
                    i - 1].k_list[getBottom(filter_k[i - 1].k_list)].k.name

                cat_model.loc[i - 1] = [code, bottom, "bottom"]
            elif(filter_k[i - 1].c_type == "r"):
                print filter_k[i - 1].bottom_k.k.name
                bottom = filter_k[
                    i - 1].k_list[getBottom(filter_k[i - 1].k_list)].k.name

                cat_model.loc[i - 1] = [code, bottom, "bottom"]
        else:
            print "bottom formate"
            print filter_k[i - 1].k.name
            cat_model.loc[i - 1] = [code, filter_k[i - 1].k.name, "bottom"]


def test(filter_k, cat_model):
    if(filter_k[- 3].top < filter_k[- 2].top > filter_k[-1].top):
        print "top"
        if isinstance(filter_k[- 2], sub_contain_k):
            print "ins", filter_k[- 2].top_k.k.name, "sell price", filter_k[- 2].bottom
            return {"sell": filter_k[- 2].bottom}
            pass
        else:
            print "k", filter_k[- 2].k.name, "sell price", filter_k[- 2].bottom
            return {"sell": filter_k[- 2].bottom}

    elif(filter_k[-3].bottom > filter_k[-2].bottom < filter_k[-1].bottom):
        print "bottom"
        if isinstance(filter_k[- 2], sub_contain_k):
            print "ins", filter_k[- 2].bottom_k.k.name, "buy price", filter_k[- 2].top
            return {"buy": filter_k[- 2].top}
            pass
        else:
            print "k", filter_k[- 2].k.name, "buy price", filter_k[- 2].top
            return {"buy": filter_k[- 2].top}
            pass

    return None


k_list = []
cat_model = pd.DataFrame([], columns=['code', 'date', 'type'])


def get_k_list(df):
    for i in range(0, df.open.count()):
        yield k(df.ix[i])

old_len = 0



def backtest(sig ,account):
    money = account[0]
    stock = account[1]
    if sig is not None:
        if(sig.has_key("buy")):
            if stock == 0:
                price = sig["buy"]
                if(money > price * 100):
                    money = money - price * 100
                    stock = 100
                else:
                    print "money not enough"
                print "money:", money
                print "stock:", stock
                account=[money,stock]
            else:
                print "can not trade"
        else:
            if(stock == 100):
                price = sig["sell"]
                money = money + 100 * price
                stock = 0
                print "money:", money
                print "stock:", stock
                account=[money,stock]
            else:
                print "can not trade"
    return account

account=[10000,0]
for i in get_k_list(df):
    k_list.append(i)
    filter_k = filter_k_list([], k_list)
    if(len(filter_k) > old_len):
        old_len = len(filter_k)
        if(len(filter_k) >= 3):
            sig = test(filter_k[-3:], cat_model)
            account=backtest(sig,account)
            #print account



