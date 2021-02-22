import sys
import os
from pathlib import Path
path_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(1, os.path.join(path_root))

import json
import scrapy
import bs4
from sina.items import SinaItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class SinaSpiderSpider(scrapy.Spider):
    name = 'sina'

    def start_requests(self):
        start_urls = []
        for k, v in get_ucodes().items():
            for v1 in v:
                if '.HK' in v1:
                    ucode = v1.replace('.HK', '').zfill(5)
                    start_urls.append({
                        'url': 'http://stock.finance.sina.com.cn/hkstock/api/openapi.php/HK_StockService.getHKPriceSummarize?symbol='+ucode,
                        'ucode': ucode})
                    start_urls.append({
                        'url': 'http://stock.finance.sina.com.cn/hkstock/api/openapi.php/HK_StockService.getHKbigDeal?symbol='+ucode,
                        'ucode': ucode})
        for data in start_urls:
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=data)

    def parse(self, response):
        item = SinaItem()
        item['ucode'] = response.meta.get('ucode')

        data = json.loads(response.body)
        if 'result' in data and 'data' in data['result']:
            data1 = data['result']['data']
            if isinstance(data1, list):
                no = 1
                for v in data['result']['data']:
                    if 'day' in v and 'symbol' in v:
                        item['stime'] = v['day']
                        item['price'] = float(v['price'])
                        item['volume'] = float(v['volume'])
                        item['pct'] = float(v['precent'])
                        item['type'] = no
                        no = no + 1
                        yield item
            elif isinstance(data1, dict):
                item['price'] = data1['avg_pri']
                item['volume'] = float(data1['volume'])
                item['volume'] = 0.0
                item['pct'] = 0.0
                item['type'] = 'avg'
                yield item
