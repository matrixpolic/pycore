from ..data_level import mysql as mysql
import copy


class data_analysis():
    """docstring for data_analysis"""

    def __init__(self, code):
        # getdata.__init__(self,code)
        self.df = mysql.select_index(code)
        self.code = code
        self.test = self.stock_ana_test()
        self.mark_result_return = self.mark_result()
        self.total_cal_return = self.total_cal()

    def stock_ana_test(self):

        df = self.df
        # code=self.code
        lis = list()

        for x in xrange(0, len(df)):
            if(df.ix[x].open >= df.ix[x].close):
                # print "open =",df.ix[x].open
                lis.append({"top": df.ix[x].open, "bottom": df.ix[
                           x].close, "name": df.ix[x]})
            else:
                # print "close =",df.ix[x].close
                lis.append({"top": df.ix[x].close, "bottom": df.ix[
                           x].open, "name": df.ix[x]})

        # return lis
        test = list()
        lim = len(lis) - 1
        for x in xrange(0, len(lis)):
            #compare(lis, x)
            # top type
            top = lis[x]['top']
            bottom = lis[x]['bottom']
            if(x + 1 <= lim):
                top_r1 = lis[x + 1]['top']
                bottom_r1 = lis[x + 1]['bottom']
            else:
                top_r1 = lis[lim]['top']
                bottom_r1 = lis[lim]['bottom']

            if(x + 2 <= lim):
                top_r2 = lis[x + 2]['top']
                bottom_r2 = lis[x + 2]['bottom']
            else:
                top_r2 = lis[lim]['top']
                bottom_r2 = lis[lim]['bottom']

            if(x + 3 <= lim):
                top_r3 = lis[x + 3]['top']
                bottom_r3 = lis[x + 3]['bottom']
            else:
                top_r3 = lis[lim]['top']
                bottom_r3 = lis[lim]['bottom']

            if(x - 1 >= 0):
                top_l1 = lis[x - 1]['top']
                bottom_l1 = lis[x - 1]['bottom']
            else:
                top_l1 = lis[0]['top']
                bottom_l1 = lis[0]['bottom']

            if(x - 2 >= 0):
                top_l2 = lis[x - 2]['top']
                bottom_l2 = lis[x - 2]['bottom']
            else:
                top_l2 = lis[0]['top']
                bottom_l2 = lis[0]['bottom']

            if(x - 3 >= 0):
                top_l3 = lis[x - 3]['top']
                bottom_l3 = lis[x - 3]['bottom']
            else:
                top_l3 = lis[0]['top']
                bottom_l3 = lis[0]['bottom']

            if(x + 5 <= lim):
                top_r5 = lis[x + 5]['top']
                bottom_r5 = lis[x + 5]['bottom']
            else:
                top_r5 = lis[lim]['top']
                bottom_r5 = lis[lim]['bottom']

            if(x + 10 <= lim):
                top_r10 = lis[x + 10]['top']
                bottom_r10 = lis[x + 10]['bottom']
            else:
                top_r10 = lis[lim]['top']
                bottom_r10 = lis[lim]['bottom']

            if(x - 5 >= 0):
                top_l5 = lis[x - 5]['top']
                bottom_l5 = lis[x - 5]['bottom']
            else:
                top_l5 = lis[lim]['top']
                bottom_l5 = lis[lim]['bottom']

            if(x - 10 >= 0):
                top_l10 = lis[x - 10]['top']
                bottom_l10 = lis[x - 10]['bottom']
            else:
                top_l10 = lis[lim]['top']
                bottom_l10 = lis[lim]['bottom']

            if((top_l1 <= top >= top_r1) and (top_l3 < top > top_r3) and (bottom_l2 < bottom > bottom_r2 or bottom_l3 < bottom > bottom_r3 or bottom_l5 < bottom > bottom_r5 or bottom_l10 < bottom > bottom_r10)):
                # print 'top type',top,bottom,df.ix[x].name
                test.append(
                    {"index": x, "value": lis[x], "attribute": "top"}
                )

            if((bottom_l1 >= bottom <= bottom_r1) and (bottom_l3 > bottom < bottom_r3) and (top_l3 > top < top_r3 or top_l2 > top < top_r2 or top_r5 > top < top_l5)):
                # print 'bottom type',top,bottom,df.ix[x].name
                test.append(
                    {"index": x, "value": lis[x], "attribute": "bottom"}
                )
        self.test = test
        return test

    def zen_result_test(self):
        #l = stock_ana(code)
        result = list()
        l = self.test
        dur = 3
        for i in l[1:-2]:
                # print l[l.index(i)-1]['index']
                # print i['index']
                # print l[l.index(i)+1]['index']
                # if (l[l.index(i)+1]['index']-i['index'])<=dur or (i['index']-l[l.index(i)-1]['index']<=dur):
                #     print i

            if (l[l.index(i) + 1]['index'] - i['index']) >= dur or (i['index'] - l[l.index(i) - 1]['index'] >= dur):
                pass
                # print i['value']['name'].name
                # l.pop(l.index(i));

        for x1 in l:
                # print x1["value"]["name"].name, x1["attribute"], len(test)
                # result.append(x1["value"]["name"])
            result.append([{x1["attribute"]:x1["value"]["name"]}])

        return result

    def mark_result(self):
        result = list()
        l = self.zen_result_test()
        l_copy = copy.deepcopy(l)
        #df = mysql.select_index(code)
        # t=l[0]
        lim = len(l) - 1
        for x in xrange(0, lim):
            mark = l[x][0].keys()[0]
        #    mark_value=l[x][0].values()[0].name
            mark_value_price = l[x][0].values()[0]
            next_mark = l[x + 1][0].keys()[0]
        #    next_mark_value=l[x+1][0].values()[0].name
            next_mark_value_price = l[x + 1][0].values()[0]
            if(mark == 'top' and next_mark == 'top'):
                # print mark_value_price.open,next_mark_value_price.open
                if(mark_value_price.open < next_mark_value_price.open):
                    # l_copy.remove(l[x])
                    l_copy[x] = 0
                else:
                    l_copy[x + 1] = 0
                pass

            if(mark == 'bottom' and next_mark == 'bottom'):
                # print mark_value_price.open,next_mark_value_price.open
                if(mark_value_price.close > next_mark_value_price.close):
                    l_copy[x] = 0
                else:
                    l_copy[x + 1] = 0
                pass
        for x in l_copy:
            if(x != 0):
                result.append(x)

        return result

    def mark_result_filter_test(self):
        l = self.mark_result_return
        df = self.df
        lim = len(l) - 1
        #print lim
        result = list()
        for x in xrange(0, lim):
            mark = l[x][0].keys()[0]
            mark_value = l[x][0].values()[0].name
            mark_value_price = l[x][0].values()[0]
            next_mark = l[x + 1][0].keys()[0]
            next_mark_value = l[x + 1][0].values()[0].name
            next_mark_value_price = l[x + 1][0].values()[0]

            if(mark == 'top' and next_mark == 'bottom'):
                dur = -df.index.tolist().index(mark_value) + \
                    df.index.tolist().index(next_mark_value)

                # result.append(l[x])
                if(dur >= 5):
                    # print mark_value,mark_value_price.open,'--fall--',next_mark_value,next_mark_value_price.close,dur
                    # print mark_value_price,next_mark_value_price
                    result.append(
                        {'fall': [mark_value_price, next_mark_value_price]})
                    # result.append(l[x])
                    # result.append(l[x+1])
                # pass
            if(mark == 'bottom' and next_mark == 'top'):
                dur = -df.index.tolist().index(mark_value) + \
                    df.index.tolist().index(next_mark_value)
                # result.append(l[x])
                if(dur >= 5):
                    # print mark_value,mark_value_price.close,'--rise--',next_mark_value,next_mark_value_price.open,dur
                    # print mark_value_price,next_mark_value_price
                    result.append(
                        {'rise': [mark_value_price, next_mark_value_price]})
                    # result.append(l[x])
                    # result.append(l[x+1])
        return result

    def filter_result(self):
        l = self.mark_result_filter_test()
        lim = len(l)
        # container=list()
        fall = list()
        rise = list()
        old_style = list()
        for x in xrange(0, lim):

            # print l[x].keys()[0]
            style = l[x].keys()[0]
            # next_style=l[x+1].keys()[0]
            value = l[x][style]
            # value_beg=value[0]
            # value_end=value[1]
            # print value_beg.open
            # print value
            # next_value=l[x+1][next_style]
            # next_value_beg=next_value[0]
            # next_value_end=next_value[1]
            # print next_value_beg.open
            # old_style=style
            if style is 'fall':
                # print x
                old_style.append(['fall', x])
                fall.append(value)
            else:
                fall.append('-')

            if style is 'rise':
                rise.append(value)
                old_style.append(['rise', x])
            else:
                rise.append('-')

        rise_filter = list()
        rise_filter_result = list()
        for x in xrange(0, len(rise)):
            if rise[x] == '-':
                # print x
                rise_filter.append(x)
                if(x == len(rise) - 1 and rise_filter != []):
                    rise_filter_result.append({'fall': rise_filter})
            else:
                rise_filter_result.append({'fall': rise_filter})
                rise_filter = []

        fall_result = rise_filter_result

        fall_filter = list()
        fall_filter_result = list()
        for x in xrange(0, len(fall)):
            if fall[x] == '-':
                # print x
                fall_filter.append(x)
                if(x == len(rise) - 1 and fall_filter != []):
                    fall_filter_result.append({'rise': fall_filter})
            else:
                fall_filter_result.append({'rise': fall_filter})
                fall_filter = []

        rise_result = fall_filter_result

        return [fall_result, rise_result]

    def total_cal(self):
        l = self.filter_result()
        fall = []
        rise = []
        total = []

        for x in l[0]:
            if x['fall'] != []:
                fall.append(x)
        for x in l[1]:
            if x['rise'] != []:
                rise.append(x)
        if rise[0]['rise'][0] == 0:
            for r in rise:
                for f in fall:
                    rise_end = r['rise'][-1] + 1
                    fall_beg = f['fall'][0]
                    if(rise_end == fall_beg):
                        total.append(r)
                        total.append(f)

            if len(total) != len(rise) + len(fall):
                for x in rise[rise.index(rise[-2]) + 1:len(rise)]:
                    total.append(x)

        elif(fall[0]['fall'][0] == 0):
            for f in fall:
                for r in rise:
                    fall_beg = f['fall'][-1] + 1
                    rise_end = r['rise'][0]

                    if(rise_end == fall_beg):
                        total.append(f)
                        total.append(r)

            if len(total) != len(rise) + len(fall):
                # print 'wrong fall',fall[fall.index(fall[-2])+1:len(fall)]
                for x in fall[fall.index(fall[-2]) + 1:len(fall)]:
                    total.append(x)

        return total
