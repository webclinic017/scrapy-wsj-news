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


class SinaPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.path_sqlite = os.path.join(self.path_root, 'data', 'aastock', 'sqlite', 'aastock.db')
        # 2.0
        self.weekday = datetime.datetime.today().weekday()
        # 3.0
        url = 'http://www.aastocks.com/tc/resources/datafeed/getstockindex.ashx?type=2'
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            last_update_time = datetime.datetime.strptime(data[0]['lastupdate'], '%Y/%m/%d %H:%M')
            self.stime = last_update_time.strftime('%Y-%m-%d')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if self.weekday in [0, 1, 2, 3, 4]:
            if 'stime' not in item:
                item['stime'] = self.stime

            conn = sqlite3.connect(self.path_sqlite)
            # 1.0 创建表
            tb_name = 's_'+item['ucode']+'_transaction_sina'
            conn.execute("CREATE TABLE IF NOT EXISTS "+tb_name+" (stime TEXT NOT NULL, ucode TEXT NOT NULL, type TEXT NOT NULL, price REAL, volume REAL, pct REAL, PRIMARY KEY (stime, ucode, type))")

            # 2.0 插值
            data = [item['stime'], item['ucode'], item['type'], item['price'], item['volume'], item['pct']]
            stmt = "REPLACE INTO "+tb_name+" (stime, ucode, type, price, volume, pct) VALUES (?, ?, ?, ?, ?, ?)"
            conn.execute(stmt, data)

            conn.commit()
            conn.close()
        return item
