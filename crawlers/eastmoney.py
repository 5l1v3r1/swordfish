#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests

class EastMoneyCrawler(object):


    ## 机构预测
    ## @param  stock_id
    ##         e.g.  sh600009
    ##
    INSTITUTION_PREDICT = "http://emweb.securities.eastmoney.com/ProfitForecast/" \
                          "ProfitForecastAjax/Index?code={}"


    ## 股票概况
    STOCK_PROFILE = "http://quote.eastmoney.com/{}.html"




    ## 盈利预测
    ## 需要 4 个参数
    ## 1. fd = date  e.g. 2017-03-31   2017-06-30  2017-09-30  2017-12-31
    ## 2. p = page   e.g. 1
    ## 3. ps = items/page e.g. 4000
    ## 4. stat = type. e.g. 1: 预增
    STOCK_PROFIT_PREDICT = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?" \
                           "type=SR&sty=YJYG&fd={}&st=2&sr=-1&p={}&ps={}&" \
                           "js=[(x)]&stat={}&rt=50258954"

    ## 日资金
    ## stock and market (1: sh, 2: sz)
    ## e.g.  DAILY_MONEY_URL.format(601801,1)
    DAILY_MONEY_URL="http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?"\
    "type=hff&rtntype=2&js=({{\"data\":[(x)]}})&cb=var%20aff_data=&check=TMLBMSPROCR&"\
    "acces_token=1942f5da9b46b069953c873404aad4b5&id={}{}"

    ## 实时价格
    #mk, 代码	名称	最新价 涨跌额	涨跌幅(%)成交量(手)	成交额(万) 振幅(%) 昨收	今开	最高	最低 换手率(%)	量比	市盈率
    #"1,600516,方大炭素,30.55,0.37,1.23,615490,1865221536,2.55,30.18,29.95,30.65,29.88,3.58,0.64,66.34"
    REALTIME_PRICE_URL="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?" \
                       "type=CT&sty=DCARQRQB&st=z&sr=&p=&ps=&cb=&js=(x)&" \
                       "token=1942f5da9b46b069953c873404aad4b5&cmd={}{}"


    REALTIME_MONEY_FLOW="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?" \
                        "type=CT&sty=CTBFTA&st=z&sr=&p=&ps=&cb=&js=(x)&" \
                        "token=70f12f2f4f091e459a279469fe49eca5&cmd={}{}"

    ## 当天的资金流记录 从开市到收市 格式如下
    #{"xa": "09:31,09:32,09:33,...,15:00,",
    # "ya": [",,,,", ",,,,", ",,,,"..., ",,,,"]}
    # xa 是 时间坐标，固定的从开市到收市
    # ya 是数据项 每个数据项包含5个域，用逗号隔开。 zlzj, cddzj, ddzj,zdzj,xdzj
    # 如果没有数据，则表现为",,,,"
    REALTIME_MONEY_FLOW_RECORD = "http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?" \
                                 "id={}{}&type=ff&check=MLBMS&cb=&js={{(x)}}&rtntype=3&" \
                                 "acces_token=1942f5da9b46b069953c873404aad4b5"

    HOME_URL = "http://www.eastmoney.com/"


    def __init__(self):
        super(EastMoneyCrawler, self).__init__()
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

    def get_institution_predict(self,stock):

        self.session.headers.update(self.headers)
        try:
            txt = self.session.get(self.INSTITUTION_PREDICT.format(stock))
            return txt.content

        except Exception as error:
            print error

        return None


    def get_stocks_predict_profit(self,date):
        self.session.headers.update(self.headers)
        try:
            txt = self.session.get(self.STOCK_PROFIT_PREDICT.format(date,1,4000,1))
            data = eval(txt.content)
            return data
        except Exception as error:
            print error

        return []


    def get_stock_profile(self,stock):
        self.session.headers.update(self.headers)
        industry = u"unknown"
        data = list()
        try:
            txt = self.session.get(self.STOCK_PROFILE.format(stock))

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(txt.content,"lxml",from_encoding = "gb18030")

            div = soup.find('div',class_="cwzb")
            line = 0
            for tr in div.table.findAll('tr')[1:3]:
                # for th in tr.findAll('th'):
                #     print th.text,
                for td in tr.findAll('td'):
                    text = td.text.replace(u"(行业平均)","")
                    text = text.replace(u"亿", "e4")
                    text = text.replace(u"千万", "e3")
                    text = text.replace(u"%", "e-2")
                    data.append(text)
                    if line == 1:
                        break

                line += 1
        except Exception as error:
            print error

        return data

    def get_realtime_price(self,stock,mk):
        """
        :param stock:
        :param mk:

        :return:
        mk,代码,名称,最新价,涨跌额,涨跌幅(%),成交量(手),成交额(万),振幅(%),昨收,今开,最高,最低,换手率(%),量比,市盈率

        1,600516,方大炭素,30.55,0.37,1.23,615490,1865221536,2.55,30.18,29.95,30.65,29.88,3.58,0.64,66.34
        """
        self.session.headers.update(self.headers)
        # print self.DAILY_MONEY_URL.format(stock,mk)
        try:
            txt = self.session.get(self.REALTIME_PRICE_URL.format(stock, mk))
            data = txt.text[1:-1]  ## get rid of the "
            return data
        except Exception as error:
            print error

        return None


    def get_realtime_money(self,stock,mk):
        """
        :param stock:
        :param mk:

        :return:
        1,600516,方大炭素,30.55,1.23%,-1174.77,3375,254080884,-267956055,-1387.52,-0.76%,
        600070912,-597943472,212.74,0.12%,565992256,-575863392,-987.11,-0.54%,411329232,
        -389710352,2161.89,1.18%,-0.64%,2017-09-29 15:00:00

        fields:
        代码	名称	最新价	涨跌幅(%)
        1,600516,方大炭素,30.55,1.23%,

        今日主力净流入,unknonw, 超大单流入,超大单流出，今日超大单净流入,超大单净比,大单流入,大单流出
        -1174.77,      3375,    254080884,-267956055,-1387.52,-0.76%,600070912,-597943472,

        今日大单净流入,大单净比,中单流入,中单流出，今日小单净流入,小单净比,小单流入,小单流出
        212.74,0.12%,565992256,-575863392,-987.11,-0.54%,411329232,-389710352,

        今日小单净流入,小单净比,时间戳
        2161.89,1.18%,-0.64%,2017-09-29 15:00:00
        """
        self.session.headers.update(self.headers)
        # print self.DAILY_MONEY_URL.format(stock,mk)
        try:
            txt = self.session.get(self.REALTIME_MONEY_FLOW.format(stock, mk))
            data = txt.text[1:-1]  ## get rid of the "
            return data
        except Exception as error:
            print error

        return None



    def get_realtime_money_record(self,stock,mk):
        """
        :param stock:
        :param mk:

        :return:
        """
        self.session.headers.update(self.headers)
        # print self.DAILY_MONEY_URL.format(stock,mk)
        try:
            txt = self.session.get(self.REALTIME_MONEY_FLOW_RECORD.format(stock,mk), timeout=(10,30))
            return txt.text
        except Exception as error:
            print error

        return None


    def get_daily_money(self,stock,mk):
        """
        :param stock: e.g.  601801
        :param mk: 1:sh   2:sz
        :return: records of daily money
        """
        self.session.headers.update(self.headers)
        #print self.DAILY_MONEY_URL.format(stock,mk)
        try:
            txt = self.session.get(self.DAILY_MONEY_URL.format(stock,mk))

            m = re.search('var aff_data=\((.+?)\)', txt.text, re.U)
            jsonText = m.group(1)
        #print jsonText
        #  date, zlzj, zljb, cddzj,cddjb, ddzj,ddjb,zdzj,zdjb,xdzj,xdjb
        #[u'2017-09-28', u'-239.7304', u'-13.37%',
        #                u'-106.3054', u'-5.93%',
        #                u'-133.425', u'-7.44%',
        #                u'58.9667', u'3.29%',
        #                u'180.7637', u'10.08%',
        #                u'12.26', u'0.16%']     ## close price, rate
            jsonObj = json.loads(jsonText)
            for rec in jsonObj['data'][0]:
                yield rec
        except Exception as err:
            print err


if __name__ == "__main__":
    eastmoney = EastMoneyCrawler()


    # for rec in eastmoney.get_daily_money('300136',2):
    #     rec = rec.replace('%','')
    #     date,zlzj,zljb,cddzj,cddjb,ddzj,ddjb,zdzj,zdjb,xdzj,xdjb,closeprice,rate = rec.split(',')
    #     print date,zlzj,zljb,closeprice
    #
    #
    #
    #
    print eastmoney.get_realtime_price('002460',2)
    #
    print eastmoney.get_realtime_money('600516', 1)
    #
    print eastmoney.get_realtime_money_record('603360', 1)

    # for rec in eastmoney.get_stock_profile("sh600516"):
    #     print rec

    data = eastmoney.get_institution_predict('sh600516')

    jsonObj = json.loads(data)

    print jsonObj['Result']['jgyc']['baseYear']
    print jsonObj['Result']['jgyc']['data'][0]

    #for d in ['2016-12-31','2017-03-31','2017-06-30','2017-09-30']:
    # for d in [ '2017-09-30']:
    #     for data in eastmoney.get_stocks_predict_profit(d):
    #         f = data.split(',')
    #         print f[0],f[1],f[-2],f[-4],f[-6]

    eastmoney.get_stock_profile('sh600987')









