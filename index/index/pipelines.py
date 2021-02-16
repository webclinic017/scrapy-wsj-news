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


class IndexPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.path_sqlite = os.path.join(self.path_root, 'data', 'aastock', 'sqlite', 'hk-marketwatch.db')
        # 2.0
        self.weekday = datetime.datetime.today().weekday()

    def process_item(self, item, spider):
        conn = sqlite3.connect(self.path_sqlite)
        tb_name = 's_' + item['ucode']
        ucode2 = '.'+item['ucode'].upper()
        if item['ucode'] == 'hstech':
            if 'turnover' in item:
                data = [item['stime'], ucode2, item['last'], item['high'], item['low'], item['turnover']]
                stmt = "REPLACE INTO "+tb_name+" (stime, code, close, high, low, turnover) VALUES (?, ?, ?, ?, ?, ?)"
                conn.execute(stmt, data)

        else:
            if 'turnover' in item:
                data = [item['turnover'], item['stime']]
                stmt = "UPDATE "+tb_name+" SET turnover=? WHERE stime=?"
                conn.execute(stmt, data)

            elif 'vol' in item:
                data = [item['stime'], ucode2, item['last'], item['high'], item['low'], item['open'], item['vol']]
                stmt = "REPLACE INTO "+tb_name+" (stime, code, close, high, low, open, volume) VALUES (?, ?, ?, ?, ?, ?, ?)"
                conn.execute(stmt, data)

        conn.commit()
        conn.close()
        return item
