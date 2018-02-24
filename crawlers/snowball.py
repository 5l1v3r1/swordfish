# -*- coding: utf-8 -*-

import requests
# from log import log
import re
import json



class SnowBall(object):
    LOGIN_PAGE = 'https://xueqiu.com/P/ZH086727'
    LOGIN_API = 'https://xueqiu.com/snowman/login'
    TRANSACTION_API = 'https://xueqiu.com/cubes/rebalancing/history.json'
    PORTFOLIO_URL = 'https://xueqiu.com/P/{}'
    WEB_REFERER = 'https://www.xueqiu.com'
    WEB_ORIGIN = ""
    LOGOUT_API = 'https://xueqiu.com/user/logout?redirect_uri=/'
    HISTORY_URL = "https://xueqiu.com/cubes/nav_daily/all.json?cube_symbol={}"
    PORTFOLIO_TOP_URL = "https://xueqiu.com/cubes/discover/rank/cube/list.json?market=cn&sale_flag=0&stock_positions=0&sort=best_benefit&category=12&profit=annualized_gain_rate&page={}&count={}"

    def __init__(self):
        super(SnowBall, self).__init__()
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Referer': self.WEB_REFERER,
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.WEB_ORIGIN,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def get_history_data(self, symbol):
        self.session.headers.update(self.headers)
        txt = self.session.get(self.HISTORY_URL.format(symbol))
        jsonObj = json.loads(txt.text)
        for k in jsonObj[:1]:  # the second list is HS300, we do not want it
            for record in k['list']:
                yield (record['date'], record['percent'], record['value'])

    def get_portfolios(self):
        self.session.headers.update(self.headers)
        for page in range(1, 11):
            txt = self.session.get(self.PORTFOLIO_TOP_URL.format(page, 40))
            jsonObj = json.loads(txt.text)
            for rec in jsonObj['list']:
                yield (rec['symbol'], rec['net_value'], rec['updated_at'],
                       rec['monthly_gain'], rec['daily_gain'], rec['annualized_gain_rate'],
                       rec['follower_count'])

    def get_current_position(self, symbol):
        self.session.headers.update(self.headers)
        txt = self.session.get(self.PORTFOLIO_URL.format(symbol))
        m = re.search('SNB.cubeTreeData =(.+?);', txt.text, re.U)
        jsonText = m.group(1)
        jsonObj = json.loads(jsonText)
        for v in jsonObj.values():
            for i, j in v.iteritems():
                if i == 'stocks':
                    for stock in j:
                        yield (stock['stock_symbol'], stock['weight'])



    def tmp(self,symbol):
        self.session.headers.update(self.headers)
        txt = self.session.get("https://xueqiu.com/P/{}".format(symbol))
        print txt.text




if __name__ == "__main__":
    snowball = SnowBall()
    for stock,weight in snowball.get_current_position("ZH010389"):
        print stock,weight


    for item in snowball.get_history_data("ZH010389"):
        print item


    print snowball.tmp("ZH010389")


    # for item in snowball.get_portfolios():
    #     print item

