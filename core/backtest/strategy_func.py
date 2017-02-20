from core.zen.k import contain_k, k, contain, contain_check, sub_contain_k

#stubborn top bottom style stratege
def only_top_bottom(filter_k, cat_model):
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