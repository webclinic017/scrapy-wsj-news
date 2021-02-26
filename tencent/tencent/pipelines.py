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


class TencentPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.path_sqlite = os.path.join(self.path_root, 'data', 'aastock', 'sqlite', 'hk-marketwatch.db')
        # 2.0
        self.weekday = datetime.datetime.today().weekday()

    def process_item(self, item, spider):
        if self.weekday in [0, 1, 2, 3, 4]:
            if 'nmll' in item and 'ucode' in item:
                conn = sqlite3.connect(self.path_sqlite)

                stmt = """INSERT INTO name (code, nmll)
                            VALUES(?, ?) 
                            ON CONFLICT(code) 
                            DO UPDATE SET nmll=?"""
                data = [item['ucode'], item['nmll'], item['nmll']]
                conn.execute(stmt, data)

                conn.commit()
                conn.close()
        return item
