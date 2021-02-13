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
from urllib.parse import urlparse
from aastock.items import AastockItem
from util.util import get_random_header, remove_line, remove_first_end_spaces, get_ucodes


class AastockSpider(scrapy.Spider):
    name = 'aastock'

    def start_requests(self):
        # 1.0
        start_urls = []
        link = 'http://wdata.aastocks.com/datafeed/getultrablocktradelog.ashx'
        for k, v in get_ucodes().items():
            for v1 in v:
                if '.HK' in v1:
                    stime1 = datetime.datetime.now().strftime('%Y%m%d')
                    stime2 = datetime.datetime.now().strftime('%Y-%m-%d')
                    ucode = v1.replace('.HK', '').zfill(5)
                    types = ['ubbull', 'bbull', 'rbull', 'ubbear', 'bbear', 'rbear']
                    for type in types:
                        url = link+'?symbol='+ucode+'&type='+type+'&lang=eng&dt='+stime1+'&f=2'
                        start_urls.append({'url': url, 'ucode': ucode, 'stime': stime2, 'type': type})
        # 2.0
        for data in start_urls:
            meta = {'ucode': data['ucode'], 'stime': data['stime']}
            yield scrapy.Request(url=data['url'], headers=get_random_header(), callback=self.parse, meta=meta)

    def parse(self, response):
        item = AastockItem()
        data = json.loads(response.body)
        if 'stat' in data:
            item['ucode'] = response.meta.get('ucode')
            item['stime'] = response.meta.get('stime')
            item['wtype'] = data['stat']['type']
            
            def format_num(val):
                if isinstance(val, float):
                    return float(val)
                elif isinstance(val, str):
                    val = str(val).lower()
                    if 'n/a' in val:
                        return float(0)
                    elif 'k' in val:
                        return float(val.replace('k', '')) * 1000
                    elif 'm' in val:
                        return float(val.replace('m', '')) * 1000000
                    elif 'b' in val:
                        return float(val.replace('b', '')) * 100000000
                    elif '%' in val:
                        return float(val.replace('%', ''))
                    elif '-' in val:
                        return float(0)
                    else:
                        return float(val)
                else:
                    return val

            item['avg'] = format_num(data['stat']['avg'])
            item['volume'] = format_num(data['stat']['volume'])
            item['turnover'] = format_num(data['stat']['turnover'])
            item['pct'] = format_num(data['stat']['pct'])
            item['pct_raw'] = format_num(data['stat']['pctRaw'])
        return item
