# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import urllib.request
import json
from time import sleep
from pathlib import Path
from datetime import datetime
from itemadapter import ItemAdapter


class WsjPipeline:
    def __init__(self):
        # 0.0 環境參數
        self.path_root = Path(__file__).parent.parent.parent
        self.cur_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        # 0.1 新數據
        self.new_data = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # 2.1 渲染頁面
        path_py = os.path.join(self.path_root, 'wsj', 'wsj', 'create_html.py')
        os.system('python '+path_py)
        sleep(10)

        # 2.2 log
        path_log = os.path.join(self.path_root, 'wsj', 'wsj', 'log', self.cur_time + '.log')
        with open(path_log, 'w', encoding='utf-8') as f:
            json.dump(self.new_data, f, ensure_ascii=False, indent=4)

        # 2.3 git
        path_git = os.path.join(self.path_root, 'run-git.bat')
        os.system(path_git)

    def process_item(self, item, spider):
        # 3.0 時間
        if 'time' in item:
            date3 = datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
            # 3.1 圖片
            if 'image_1' in item:
                # 3.1.1 路徑
                path3_1 = os.path.join(self.path_root, 'data', 'wsj', date3, 'img')
                Path(path3_1).mkdir(parents=True, exist_ok=True)
                # 3.1.2 儲存
                path3_2 = os.path.join(path3_1, item['image_1'])
                if not os.path.exists(path3_2):
                    urllib.request.urlretrieve(item['image_1_url'], path3_2)
            # 3.2 json
            if 'url' in item and 'title' in item:
                # 3.2.1 路徑
                path3_3 = os.path.join(self.path_root, 'data', 'wsj', date3, 'json')
                Path(path3_3).mkdir(parents=True, exist_ok=True)
                # 3.2.2 儲存
                path3_4 = os.path.join(path3_3, item['url']+'.json')
                if not os.path.exists(path3_4):
                    with open(path3_4, 'w', encoding='utf-8') as f:
                        self.new_data.append(str(item['title']))
                        json.dump(dict(item), f, ensure_ascii=False, indent=4)
        return item
