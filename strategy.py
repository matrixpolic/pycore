from k import contain_k, k, contain, contain_check, sub_contain_k
import core.data_level.mysql as mysql
import pandas as pd


def get_k_list(df):
    for i in range(0, df.open.count()):
        yield k(df.ix[i])


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


def tb_cal(filter_k, cat_model, code):
        #contain_check(filter_k[i-1], filter_k[i])
    # for i in range(0,len(filter_k)):
    #     if i>=2:
    i = -1
    if(filter_k[i - 2].top < filter_k[i - 1].top > filter_k[i].top):
        if isinstance(filter_k[i - 1], sub_contain_k):
                    # print "top formate sub_contain_k"
            if(filter_k[i - 1].c_type == "l"):
                        # print filter_k[i - 1].top_k.k.name
                date_top = filter_k[
                    i - 1].k_list[getTop(filter_k[i - 1].k_list)].k.name
                # test max
                # test=filter_k[i-1].k_list
                ins = filter_k[i - 1]
                return [code, date_top, "top", ins]

            elif(filter_k[i - 1].c_type == "r"):
                # print filter_k[i - 1].top_k.k.name
                date_top = filter_k[
                    i - 1].k_list[getTop(filter_k[i - 1].k_list)].k.name

                ins = filter_k[i - 1]
                return [code, date_top, "top", ins]
        else:
            # print "top formate"
            # print filter_k[i - 1].k.name

            ins = filter_k[i - 1]
            return [code, filter_k[i - 1].k.name, "top", ins]

    elif(filter_k[i - 2].bottom > filter_k[i - 1].bottom < filter_k[i].bottom):
        if isinstance(filter_k[i - 1], sub_contain_k):
            # print "bottom formate sub_contain_k"
            if(filter_k[i - 1].c_type == "l"):
                # print filter_k[i - 1].bottom_k.k.name

                bottom = filter_k[
                    i - 1].k_list[getBottom(filter_k[i - 1].k_list)].k.name

                ins = filter_k[i - 1]
                return [code, bottom, "bottom", ins]
            elif(filter_k[i - 1].c_type == "r"):
                # print filter_k[i - 1].bottom_k.k.name
                bottom = filter_k[
                    i - 1].k_list[getBottom(filter_k[i - 1].k_list)].k.name

                ins = filter_k[i - 1]
                return [code, bottom, "bottom", ins]
        else:
            # print "bottom formate"
            # print filter_k[i - 1].k.name

            ins = filter_k[i - 1]
            return [code, filter_k[i - 1].k.name, "bottom", ins]

    return None

strategy_mark = []


def mark_list_cal(strategy_list):
    if len(strategy_list) >= 2:
        last_strategy_list = strategy_list[-1]
        c_type = last_strategy_list[2]
        date = last_strategy_list[1]
        num = last_strategy_list[4]
        if(len(strategy_mark) >= 1):
            last_strategy_mark = strategy_mark[-1]
            last_strategy_mark_c_type = last_strategy_mark[2]
            last_strategy_mark_date = last_strategy_mark[1]
            last_strategy_mark_num = last_strategy_mark[4]
            # print last_strategy_mark_c_type
            if last_strategy_mark_c_type != c_type:
                if (num - last_strategy_mark_num) >= 5:
                    print last_strategy_mark
                    print last_strategy_list
                    strategy_mark.append(last_strategy_list)

                elif(num - last_strategy_mark_num) == 1:
                    print "----==1--"
                    print last_strategy_mark
                    print last_strategy_list
                    pass
                else:
                    print "no sig", last_strategy_list
            else:
                print "no sig", last_strategy_list
        else:
            strategy_mark.append(last_strategy_list)

        # pass

        # middle channel
# line class


class line(object):
    """docstring for line"""

    def __init__(self, begin_point, end_point):
        self.begin_point = begin_point
        self.begin_point_type = begin_point[2]
        self.begin_point_date=begin_point[1]
        self.begin_point_k = begin_point[3]
        self.end_point = end_point
        self.end_point_type = end_point[2]
        self.end_point_date = end_point[1]
        self.end_point_k = end_point[3]
        self.ana_line()

    def ana_line(self):
        if self.begin_point_type == "top" and self.end_point_type == "bottom":
            self.line_type = "fall"
            self.line_top = self.begin_point_k.top
            self.line_bottom = self.end_point_k.bottom
            self.begin_pirce = self.begin_point_k.top
            self.end_priece = self.end_point_k.bottom
        elif self.begin_point_type == "bottom" and self.end_point_type == "top":
            self.line_type = "rise"
            self.line_top = self.begin_point_k.bottom
            self.line_bottom = self.end_point_k.top
            self.begin_pirce = self.begin_point_k.bottom
            self.end_priece = self.end_point_k.top
        else:
            print "error"

        pass

# middle channel calss


class mid_channel_test(object):
    """docstring for mid_channel"""

    def __init__(self, line1,line2,line3):
        self.mid_channel_contain=[]
        self.same_price_area(line1, line2, line3)
        self.line1=line1
        if(self.mid_channel_area!=None):
            self.mid_channel_uprim=max(self.mid_channel_area )
            self.mid_channel_downrim=min(self.mid_channel_area )

    def same_price_area(self,line1, line2, line3):
        print "{"
        print line1.line_top, line1.line_bottom, line1.line_type
        print line2.line_top, line2.line_bottom, line2.line_type
        print line3.line_top, line3.line_bottom, line3.line_type
        print "----"
        print line1.begin_point_date, line1.end_point_date, line1.line_type
        print line2.begin_point_date, line2.end_point_date, line2.line_type
        print line3.begin_point_date, line3.end_point_date, line3.line_type
        print "}"
        l123_l_type = [line1.line_type,
                       line2.line_type,
                       line3.line_type]
        if l123_l_type==["fall","rise","fall"]:
            if line3.end_priece>line1.begin_pirce:
                print "error"
                self.mid_channel_area=None
            else:
                top_point=[line1.begin_pirce,line3.begin_pirce]
                bottom_point=[line1.end_priece,line3.end_priece]
                print "fall", min(top_point),max(bottom_point)

                self.mid_channel_area=[min(top_point),max(bottom_point)]
                return [min(top_point),max(bottom_point)]
        if l123_l_type==["rise","fall","rise"]:
            if line3.end_priece<line1.begin_pirce:
                print "error"
                self.mid_channel_area=None
            else:
                top_point=[line1.begin_pirce,line3.begin_pirce]
                bottom_point=[line1.end_priece,line3.end_priece]
                print "rise",min(top_point),max(bottom_point)

                self.mid_channel_area=[min(top_point),max(bottom_point)]
                return [min(top_point),max(bottom_point)]

    def ext(self,line):
        self.mid_channel_contain.append(line)


# lines=[]

def draw_line(lines, strategy_list):
    if len(strategy_list) >= 2:
        begin_point = strategy_list[-2]

        end_point = strategy_list[-1]
        return line(begin_point, end_point)

    pass


def same_price_area(line1, line2, line3):
    print "{"
    print line1.line_top, line1.line_bottom, line1.line_type
    print line2.line_top, line2.line_bottom, line2.line_type
    print line3.line_top, line3.line_bottom, line3.line_type
    print "----"
    print line1.begin_pirce, line1.end_priece, line1.line_type
    print line2.begin_pirce, line2.end_priece, line2.line_type
    print line3.begin_pirce, line3.end_priece, line3.line_type
    print "}"
    l123_l_type = [line1.line_type,
                   line2.line_type,
                   line3.line_type]
    if l123_l_type==["fall","rise","fall"]:
        if line3.end_priece>line1.begin_pirce:
            print "error"
        else:
            top_point=[line1.begin_pirce,line3.begin_pirce]
            bottom_point=[line1.end_priece,line3.end_priece]
            print "fall", min(top_point),max(bottom_point)
            return [min(top_point),max(bottom_point)]
    if l123_l_type==["rise","fall","rise"]:
        if line3.end_priece<line1.begin_pirce:
            print "error"
        else:
            top_point=[line1.begin_pirce,line3.begin_pirce]
            bottom_point=[line1.end_priece,line3.end_priece]
            print "rise",min(top_point),max(bottom_point)
            return [min(top_point),max(bottom_point)]

mid_channel_list=[]
def draw_mid_channel(lines_list):
    if(len(lines_list) >= 3) and len(mid_channel_list)==0:
        line1 = lines_list[-3]
        line2 = lines_list[-2]
        line3 = lines_list[-1]
        mid_channel=mid_channel_test(line1, line2, line3)
        if(mid_channel.mid_channel_area!=None):
            print "mid channel create"
            mid_channel_list.append(mid_channel)
    else:
        if len(mid_channel_list)>=1:
            line1 = lines_list[-3]
            line2 = lines_list[-2]
            line3 = lines_list[-1]

            mid_channel=mid_channel_list[-1]
            mid_channel_uprim=mid_channel.mid_channel_uprim
            mid_channel_downrim=mid_channel.mid_channel_downrim
            if line3.line_top>mid_channel_uprim and line3.line_bottom<mid_channel_downrim:
                print "mid channel extends",line3.line_top,line3.line_bottom,mid_channel.mid_channel_area,line3.begin_point_date,line3.end_point_date
                mid_channel.ext(line3)
            elif line3.line_top>mid_channel_uprim and line3.line_bottom>mid_channel_uprim:
                if isinstance(line3.begin_point_k, k):
                    #print line3.begin_point_k
                    pass
                else:
                    print "all line up mid channel",line3.line_top,line3.line_bottom,mid_channel.mid_channel_area,line3.begin_point_date
            else:
                print line3.begin_point_date,line3.end_point_date
    pass


code = "000009"
df = mysql.select_basd_on_code(code)


old_len = 0

k_list = []
lines_list = []

cat_model = pd.DataFrame([], columns=['code', 'date', 'type'])

strategy_list = []

account = [10000, 0]
for i in get_k_list(df[:100]):
    k_list.append(i)
    filter_k = filter_k_list([], k_list)
    if(len(filter_k) > old_len):
        old_len = len(filter_k)
        if(len(filter_k) >= 3):
            mark_list = tb_cal(filter_k[-3:], cat_model, code)
            if mark_list != None:
                # print mark_list[2]
                mark_list.append(filter_k.index(mark_list[3]))
                strategy_list.append(mark_list)
                # print strategy_list
                # mark_list_cal(strategy_list)
                if(len(strategy_list) >= 2):
                    lines_list.append(draw_line([], strategy_list))
                    draw_mid_channel(lines_list)
