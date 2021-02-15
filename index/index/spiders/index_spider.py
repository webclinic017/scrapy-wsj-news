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


class IndexSpiderSpider(scrapy.Spider):
    name = 'index_spider'

    def start_requests(self):
        start_urls = ['http://www.aastocks.com/en/stocks/market/index/hk-index.aspx']
        for data in start_urls:
            meta = {}
            yield scrapy.Request(url=data, headers=get_random_header(), callback=self.parse, meta=meta)

    def parse(self, response):
        item = IndexItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')

        tb = html.find('table', {'class': 'tblM'})

        data3 = tb.find('td', {'class': 'txt_l'})
        stime = data3.getText().split("\r")[1].split("Update")[1].replace(': ', '')
        stime2 = datetime.datetime.strptime(stime, '%Y/%m/%d %H:%M')
        item['stime'] = stime2.strftime('%Y-%m-%d')

        for v1 in tb.find_all('tr', {'class': 'tblM_row'}):
            data2 = v1.find_all('td')
            if len(data2) == 8:
                item['ucode'] = data2[0].getText().lower()

                if item['ucode'] == 'hs tech':
                    item['ucode'] = 'hstech'
                elif item['ucode'] == 'hscei':
                    item['ucode'] = 'hsce'

                item['last'] = float(data2[1].getText().replace('▼', '').replace('▲', '').replace(',', ''))
                item['chng'] = float(data2[2].getText().replace('+', ''))
                item['pchng'] = float(data2[3].getText().replace('+', '').replace('%', ''))
                item['turnover'] = data2[4].getText().replace(',', '').lower()
                if 'm' in item['turnover']:
                    item['turnover'] = float(item['turnover'].replace('m', ''))*1000000
                elif 'b' in item['turnover']:
                    item['turnover'] = float(item['turnover'].replace('b', ''))*1000000000
                item['high'] = data2[5].getText().replace(',', '').lower()
                item['low'] = data2[6].getText().replace(',', '').lower()
                yield item
