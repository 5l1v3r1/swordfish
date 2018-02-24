#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

class PhenixCrawler(object):

    HOME_URL = "http://hq.finance.ifeng.com"

    REALTIME_PRIC_URL = "http://hq.finance.ifeng.com/q.php?l={}"

    def __init__(self):
        super(PhenixCrawler, self).__init__()
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Referer': self.HOME_URL,
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.HOME_URL,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

    ##
    #  @param   stocks   list of stock
    #           e.g.   ['sh600009','sh000001']
    #
    #  @return  dataframe
    #
    def get_realtime_price(self,stocks):

        self.session.headers.update(self.headers)
        stocklist = ",".join(stocks)
        txt = self.session.get(self.REALTIME_PRIC_URL.format(stocklist),timeout=30)
        json_str = txt.text[len("var json_q="):]
        n = json_str.rfind(';')
        json_str = json_str[:n]
        jsonObj = json.loads(json_str)
        for k in jsonObj.keys():
            yield (k,jsonObj[k])





# if __name__ == "__main__":
#     from get_stock_profile import get_stocks
#     import sys
#     sys.path.append("..")
#     from com.dbUtility import get_conn
#     with get_conn() as conn:
#         cnt = 1
#         crawler = PhenixCrawler()
#         for stock,data in crawler.get_realtime_price(get_stocks(conn)):
#             #print cnt,stock,data
#             cnt += 1
