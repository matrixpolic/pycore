# -*- coding: utf-8 -*-
from ..data_level import mysql as mysql
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts


class article(object):
    """docstring for article"""

    def __init__(self):
    	self.mark=-1
    	self.tdb_mark=self.mark-1
        self.get_date()
        pass

    def get_date(self):
        self.sh = mysql.select_index('sh')
        self.end_day = self.sh.ix[self.mark].name
        self.day_before_end = self.sh.ix[self.tdb_mark].name
        self.end_day_data = mysql.select_day_mark(self.end_day)
        self.day_before_end_data = mysql.select_day_mark(self.day_before_end)

    def date_restructure(self, total):
        dic = {'jump': total.loc[total['type'] == 'jump'],
               'low': total.loc[total['type'] == 'low'],
               'high': total.loc[total['type'] == 'high'],
               'ab_high': total.loc[total['type'] == 'ab_high'],
               'ab_low': total.loc[total['type'] == 'ab_low']}
        return dic

    def date_filter(self):
        dic = self.date_restructure(self.end_day_data)
        dic_yes = self.date_restructure(self.day_before_end_data)
        # 昨天新低，今天继续新低
        yestod = [i for i in dic_yes['low'].code.tolist() if i in dic[
            'low'].code.tolist()]
        # 今天新进入新低
        tod = [i for i in dic['low'].code.tolist() if i not in yestod]
        # 昨天涨了
        yes_ris = [i for i in dic_yes['low'].code.tolist() if i not in yestod]
        return {'yestod': yestod, 'tod': tod, 'yes_ris': yes_ris}

    def content(self):
        dic = self.date_restructure(self.end_day_data)
        total = self.end_day_data
        content = '今日开盘总共:' + str(len(total)) + '只股票<br>统计数据：处于震荡区的股票有:' + str(len(dic['jump'])) + "只;</p>" + "处于高位的股票有:" + str(len(dic['high'])) + "只;</p>" + "处于低位的股票有:" + str(
            len(dic['low'])) + "只;</p>" + "处于绝对高位的股票有:" + str(len(dic['ab_high'])) + "只;</p>" + "处于绝对低位的股票有:" + str(len(dic['ab_low'])) + "只;</p>"
        focus = '关注以下股票:<br>'
        x = 0
        for i, row in dic['low'].iterrows():
            # print 'guanzhu'+str(row['code'])
            focus += '<a href="http://localhost/code/?code=' + \
                str(row['code']) + '">' + str(row['code']) + '</a>,'
            x += 1
            if x % 9 == 0:
                focus += '<p>'
        content += focus
        #-----
        result = self.date_filter()
        x = 0
        conclude = "<p>细节分析：<p>"
        conclude += "昨日低位股票，今日继续保持低位的有：<p>"
        for i in result['yestod']:
            conclude += '<a href="http://localhost/code/?code=' + \
                str(i) + '">' + str(i) + '</a>,'
            x += 1
            if x % 9 == 0:
                conclude += '<p>'
        conclude += "<p>今日新进入低位的股票：<p>"
        x = 0
        for i in result['tod']:
            conclude += '<a href="http://localhost/code/?code=' + \
                str(i) + '">' + str(i) + '</a>,'
            x += 1
            if x % 9 == 0:
                conclude += '<p>'
        conclude += "<p>昨日推荐低位股票，今日上涨的股票有：<p>"
        x = 0
        for i in result['yes_ris']:
            conclude += '<a href="http://localhost/code/?code=' + \
                str(i) + '">' + str(i) + '</a>,'
            x += 1
            if x % 9 == 0:
                conclude += '<p>'
        content += conclude
        return content

    def wordpress(self):
        wp = Client('http://localhost/xmlrpc.php',
                    'client', 'GJyh2vs(AT*He&F#WdEzgdnN')
        post = WordPressPost()
        post.title = str(self.end_day) + '盘后总结'
        post.content = self.content()
        post.post_status = 'publish'
        wp.call(NewPost(post))


