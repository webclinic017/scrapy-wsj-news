import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import scrapy
import bs4
import re
from yahoo.items import YahooItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class YahooSpiderSpider(scrapy.Spider):
    name = 'yahoo'

    def start_requests(self):
        start_urls = []
        for k, v in get_ucodes().items():
            for v1 in v:
                if '.HK' in v1:
                    ucode = v1.replace('.HK', '').zfill(4)
                    ucode2 = v1.replace('.HK', '').zfill(5)
                    url = 'https://finance.yahoo.com/quote/'+ucode+'.HK?p='+ucode+'.HK&.tsrc=fin-srch'
                    start_urls.append({'url': url, 'ucode': ucode2})

        # start_urls = [{'url': 'https://finance.yahoo.com/quote/1024.HK?p=1024.HK&.tsrc=fin-srch', 'ucode': '01024'}]
        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=data)

    def parse(self, response):
        item = YahooItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')
        item['ucode'] = response.meta.get('ucode')

        for v3 in html.find_all('span', {'class': 'Trsdu(0.3s)'}):
            if v3['data-reactid'] == '32':
                item['last'] = float(v3.getText().replace(',', ''))
            elif v3['data-reactid'] == '33':
                temp1 = v3.getText().split()
                if len(temp1) == 2:
                    item['chng'] = float(temp1[0])
                    if temp1[1]:
                        item['pchng'] = float(temp1[1].replace('+', '').replace('%', '').replace('(', '').replace(')', ''))
            elif v3['data-reactid'] == '47':
                item['open'] = float(v3.getText().replace('%', ''))

        for v4 in html.find_all('td', {'class': 'Ta(end)'}):
            if v4['data-reactid'] == '61':
                temp2 = v4.getText().split()
                item['high'] = float(temp2[0])
                item['low'] = float(temp2[2])
            elif v4['data-reactid'] == '69':
                item['vol'] = float(re.sub(r",", '', v4.getText()))
            elif v4['data-reactid'] == '92':
                if v4.getText() == 'N/A':
                    item['pe'] = 'N/A'
                else:
                    item['pe'] = float(v4.getText())
            elif v4['data-reactid'] == '97':
                if v4.getText() == 'N/A':
                    item['eps'] = 'N/A'
                else:
                    item['eps'] = float(v4.getText())

        return item
