import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import scrapy
import bs4
import re
import datetime
from index.items import IndexItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class YahooSpiderSpider(scrapy.Spider):
    name = 'yahoo_spider'

    def start_requests(self):
        start_urls = [{'ucode': 'hsi', 'url': 'https://hk.finance.yahoo.com/quote/%5EHSI/history?p=%5EHSI'},
                      {'ucode': 'hsce', 'url': 'https://hk.finance.yahoo.com/quote/%5EHSCE/history?p=%5EHSCE'},
                      {'ucode': 'dji', 'url': 'https://hk.finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI'},
                      {'ucode': 'sp500', 'url': 'https://hk.finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC'}]
        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=data)

    def parse(self, response):
        item = IndexItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')
        item['ucode'] = response.meta.get('ucode')

        tb = html.find('table', {'data-test': 'historical-prices'})
        for tr in tb.find_all('tr'):
            td = tr.find_all('td')
            if len(td) == 7:
                item['stime'] = datetime.datetime.strptime(td[0].getText(), '%Y年%m月%d日')
                item['stime'] = item['stime'].strftime('%Y-%m-%d')
                if not td[1].getText() == '-':
                    item['open'] = float(td[1].getText().replace(',', ''))
                    item['high'] = float(td[2].getText().replace(',', ''))
                    item['low'] = float(td[3].getText().replace(',', ''))
                    item['last'] = float(td[4].getText().replace(',', ''))
                    item['vol'] = float(td[6].getText().replace(',', ''))
                    yield item
