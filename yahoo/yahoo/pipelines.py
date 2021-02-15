# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import urllib.request
import json
import sqlite3 as sqlite3
import os
import datetime


class YahooPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.path_sqlite = os.path.join(self.path_root, 'data', 'aastock', 'sqlite', 'hk-yahoo.db')
        # 2.0
        self.weekday = datetime.datetime.today().weekday()
        # 3.0
        url = 'http://www.aastocks.com/tc/resources/datafeed/getstockindex.ashx?type=2'
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            last_update_time = datetime.datetime.strptime(data[0]['lastupdate'], '%Y/%m/%d %H:%M')
            self.stime = last_update_time.strftime('%Y-%m-%d')
            self.err = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        print(len(self.err), self.err)
        pass

    def process_item(self, item, spider):
        conn = sqlite3.connect(self.path_sqlite)
        tb_name = 's_' + item['ucode']

        if 'ucode' in item and 'last' in item and 'high' in item and 'low' in item and 'open' in item and 'vol' in item:
            data = [self.stime, item['ucode'], item['last'], item['high'], item['low'], item['open'], item['vol'],]
            stmt = "REPLACE INTO "+tb_name+" (stime, code, close, high, low, open, volume) VALUES (?, ?, ?, ?, ?, ?, ?)"
            conn.execute(stmt, data)
        else:
            self.err.append(item['ucode'])

        conn.commit()
        conn.close()
        return item
