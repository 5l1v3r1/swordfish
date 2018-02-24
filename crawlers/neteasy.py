#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
import requests

class NetEasy(object):
    """
    网易财经
    """

    HOME_URL = "http://quotes.money.163.com"

    ANNUAL_REPORT_URL = "http://quotes.money.163.com/service/xjllb_{}.html?type=year"

    STOCK_PROFILE_URL = "http://quotes.money.163.com/{}{}.html"  ## mk: 0/1 stock: 600987

    tmp_URL = "http://quote.eastmoney.com/sh600987.html"

    ## price "http://api.money.126.net/data/feed/1002202,0600987,money.api?callback=data"

    def __init__(self):
        super(NetEasy, self).__init__()
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



    def get_annual_report(self,stock):
        df = pd.read_csv('http://quotes.money.163.com/service/xjllb_{}.html?type=year'.format(stock[2:]),
                         header=0,index_col=0)

        df.replace('--',0,inplace=True)


        df.index = pd.Index(map(lambda x:x.decode('gb2312').strip().replace(u'(万元)',''),df.index.values))

        return df


    def get_stock_profile(self,stock):
        self.session.headers.update(self.headers)
        try:
            if stock[:2] == 'sh':
                mk = 0
            else:
                mk = 1
            #txt = self.session.get(self.STOCK_PROFILE_URL.format(mk,stock[2:]))
            txt = self.session.get("http://quote.eastmoney.com/{}.html".format(stock))
            #print txt.content
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(txt.content, "lxml", from_encoding="gb18030")
            table = soup.find('table', id="rtp2")
            div = table.find('span', id="gt13_2")
            for row in table.findAll("tr"):
                cells = row.findAll("td")
                for cell in cells:
                    attr,value = cell.text.split(u'：')
                    print attr, value


        except Exception as error:
            print error






if __name__ == "__main__":

    crawler = NetEasy()
    stocks = ['sh600987','sh600009']

    crawler.get_stock_profile(stocks[0])

    #
    #
    # names = [u'经营活动产生现金流量净额', u'处置固定资产、无形资产和其他长期资产的损失',
    #          u'固定资产折旧、油气资产折耗、生产性物资折旧', u'无形资产摊销', u'长期待摊费用摊销']
    #
    # for stock in stocks:
    #     df = crawler.get_annual_report(stock)
    #
    #
    #     dates = df.columns.values[:-1]
    #
    #     for d in dates:
    #         sum = 0
    #         #print '[',d,']'
    #         for i in range(1,len(names)):
    #             #print names[i]
    #             sum += int(df.ix[names[i]][d])
    #
    #         cash = int(df.ix[names[0]][d])  - sum
    #         df.set_value('net_cash',d,cash)
    #
    #     sdata = df.ix['net_cash'].dropna()
    #     for k in sdata.index:
    #         print stock, k, sdata[k]




