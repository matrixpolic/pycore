import core.data_level.mysql as mysql
import pandas as pd
from core.zen.k import contain_k, k, contain, contain_check, sub_contain_k


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

def get_k_list(df):
    for i in range(0, df.open.count()):
        yield k(df.ix[i])


#stubborn top bottom style stratege
def top_bottom(filter_k, cat_model,code):
    if(filter_k[- 3].top < filter_k[- 2].top > filter_k[-1].top):
        #print "top"
        if isinstance(filter_k[- 2], sub_contain_k):
            #print "ins", filter_k[- 2].top_k.k.name, "sell price", filter_k[- 2].bottom
            return [code,filter_k[- 2].top_k.k.name,filter_k[- 2].top,"top"]
            # return {"sell": filter_k[- 2].bottom}
            pass
        else:
            #print "k", filter_k[- 2].k.name, "sell price", filter_k[- 2].bottom
            return [code,filter_k[- 2].k.name,filter_k[- 2].top,"top"]
            # return {"sell": filter_k[- 2].bottom}

    elif(filter_k[-3].bottom > filter_k[-2].bottom < filter_k[-1].bottom):
        #print "bottom"
        if isinstance(filter_k[- 2], sub_contain_k):
            #print "ins", filter_k[- 2].bottom_k.k.name, "buy price", filter_k[- 2].top
            return [code,filter_k[- 2].bottom_k.k.name,filter_k[- 2].bottom,"bottom"]
            # return {"buy": filter_k[- 2].top}
            pass
        else:
            #print "k", filter_k[- 2].k.name, "buy price", filter_k[- 2].top
            return [code,filter_k[- 2].k.name,filter_k[- 2].bottom,"bottom"]
            # return {"buy": filter_k[- 2].top}
            pass

    return None

def get_top_down(code="000009",table="top_bottom_stock"):

	#code = code
	df = mysql.select_basd_on_code(code)
	k_list = []
	cat_model = pd.DataFrame([], columns=['code', 'date', "price",'type'])
	old_len = 0

	top_bottom_list=[]
	for i in get_k_list(df):
	    k_list.append(i)
	    filter_k = filter_k_list([], k_list)
	    if(len(filter_k) > old_len):
	        old_len = len(filter_k)
	        if(len(filter_k) >= 3):
	    	    new= top_bottom(filter_k[-3:], cat_model,code)
	    	    #print new
	    	    if(new !=None):
	    		   top_bottom_list.append(new)


	cat_model = pd.DataFrame(top_bottom_list, columns=['code', 'date', "price",'type'])
	return cat_model
	#mysql.insert_tab(cat_model, table)


df=get_top_down()

