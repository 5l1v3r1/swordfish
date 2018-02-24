#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests

class SinaCrawler(object):

    HOME_URL = "http://finance.sina.com.cn/stock/"

    REALTIME_PRIC_URL = "http://hq.sinajs.cn/list={}"

    def __init__(self):
        super(SinaCrawler, self).__init__()
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
        try:
            stocklist = ",".join(stocks)
            txt = self.session.get(self.REALTIME_PRIC_URL.format(stocklist))
            for line in txt.content.split(";"):
                if len(line) > 10:
                    (stock, data) = line.split('=')
                    yield stock[-8:],str(data[1:-1]).split(',')

        except Exception as error:
            print error



if __name__ == "__main__":
    crawler = SinaCrawler()
    for stock,data in crawler.get_realtime_price(['sh600009','sz002202']):
        print stock,data[3],data[8],data[9],data[6],data[10],data[7],data[20]

    from crawlers.phenix import PhenixCrawler
    crawler = PhenixCrawler()
    for stock, data in crawler.get_realtime_price(['sh600009', 'sz002202']):
        print stock, data[0], data[9], data[10], data[11], data[16], data[21], data[26]

