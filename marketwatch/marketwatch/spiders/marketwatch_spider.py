import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import scrapy
import bs4
import datetime
import re
from marketwatch.items import MarketwatchItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class MarketwatchSpiderSpider(scrapy.Spider):
    name = 'marketwatch_spider'

    def start_requests(self):
        start_urls = []
        for k, v in get_ucodes().items():
            for v1 in v:
                if k == '指數ETF' or k == '指數ETFx' or k == '反向指數ETFx':
                    ucode = v1.replace('.HK', '').zfill(4)
                    url = 'https://www.marketwatch.com/investing/fund/'+ucode+'/download-data?countrycode=hk&mod=mw_quote_tab'
                    start_urls.append({'url': url, 'ucode': ucode+'.HK', 'tb_name': ucode.zfill(5)})
                elif k == '美國ETF':
                    ucode = v1
                    url = f'https://www.marketwatch.com/investing/fund/{ucode}/download-data?mod=mw_quote_tab'
                    start_urls.append({'url': url, 'ucode': ucode, 'tb_name': ucode})
                elif '.HK' in v1:
                    ucode = v1.replace('.HK', '').zfill(4)
                    url = 'https://www.marketwatch.com/investing/stock/'+ucode+'/download-data?countrycode=hk&mod=mw_quote_tab'
                    start_urls.append({'url': url, 'ucode': ucode+'.HK', 'tb_name': ucode.zfill(5)})
                elif '.O' in v1 or '.K' in v1:
                    ucode = v1.replace('.O', '').replace('.K', '').lower()
                    url = 'https://www.marketwatch.com/investing/stock/'+ucode+'/download-data?mod=mw_quote_tab'
                    ucode2 = v1.replace('.', '').lower()
                    start_urls.append({'url': url, 'ucode': v1, 'tb_name': ucode2})
                elif '.SS' in v1 or '.SZ' in v1:
                    ucode = v1.replace('.SS', '').replace('.SZ', '').lower()
                    url = 'https://www.marketwatch.com/investing/stock/'+ucode+'/download-data?countryCode=CN'
                    if ucode == '000016': # 上證50
                        url = 'https://www.marketwatch.com/investing/index/'+ucode+'/download-data?countrycode=cn&mod=mw_quote_tab'
                    start_urls.append({'url': url, 'ucode': v1, 'tb_name': ucode})
                elif k == '指數2':
                    url = 'https://www.marketwatch.com/investing/index/'+v1+'/download-data?countrycode=xx&mod=mw_quote_tab'
                    start_urls.append({'url': url, 'ucode': v1, 'tb_name': v1})

        # start_urls = [{'url': 'https://www.marketwatch.com/investing/stock/6618/download-data?countrycode=hk&mod=mw_quote_tab', 'ucode': '06618'}]
        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=data)

    def parse(self, response):
        item = MarketwatchItem()
        html = bs4.BeautifulSoup(response.body, 'lxml')
        item['ucode'] = response.meta.get('ucode')
        item['tb_name'] = response.meta.get('tb_name')

        data = html.find_all('div', {'class': 'download-data'})
        if data:
            for v1 in [data[0]]:
                for v2 in v1.find_all('tr', {'class': 'table__row'}):
                    stime = v2.find('div', {'class': 'fixed--cell'})
                    if stime is not None and len(list(stime.getText())) == 10:
                        stime2 = datetime.datetime.strptime(stime.getText(), '%m/%d/%Y')
                        item['stime'] = stime2.strftime('%Y-%m-%d')
                        v3 = v2.find_all('td', {'class': 'overflow__cell'})
                        for i in [1, 2, 3, 4, 5]:
                            if i >= len(v3):
                                break
                            v4 = float(v3[i].getText().replace('HK', '').replace('$', '').replace(',', '').replace('¥', ''))
                            if i == 1:
                                item['open'] = v4
                            elif i == 2:
                                item['high'] = v4
                            elif i == 3:
                                item['low'] = v4
                            elif i == 4:
                                item['last'] = v4
                            elif i == 5:
                                item['vol'] = v4
                        if 'vol' not in item:
                            item['vol'] = 0
                        yield item
