import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import json
import scrapy
import bs4
import re
import datetime
from index.items import IndexItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class YahooSpiderSpider(scrapy.Spider):
    name = 'reuters_spider'

    def start_requests(self):
        start_urls = ['https://www.reuters.com/companies/api/getFetchQuotes/.DJI,.SPX,.IXIC,.HSI,.HSCE,.SSEC,.CSI300,.FTSE,.GDAXI,.FCHI,.N225,.TWII,.KS11']
        for url in start_urls:
            yield scrapy.Request(url=url, headers=get_random_header(), callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        for v in data['market_data']['indices']:
            item = IndexItem()
            item['ucode'] = v['ric'].replace('.', '').lower()
            if item['ucode'] == 'spx':
                item['ucode'] = 'sp500'
            item['last'] = float(v['last'])
            if v['net_change']:
                item['chng'] = float(v['net_change'])
            if v['percent_change']:
                item['pchng'] = float(v['percent_change'])
            if v['day_high']:
                item['high'] = float(v['day_high'])
            if v['day_low']:
                item['low'] = float(v['day_low'])
            if v['open']:
                item['open'] = float(v['open'])
            if v['volume']:
                item['vol'] = int(v['volume'])
            if v['modified']:
                item['stime'] = datetime.datetime.strptime(v['modified'], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
            yield item
