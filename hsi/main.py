import requests
import os
import io
import pandas as pd
import win32com
import win32com.client
import numpy as np
from pathlib import Path
from time import sleep
from datetime import datetime
os.system('taskkill /F /IM wps.exe ')

# 1.0
url = 'https://www.hsi.com.hk/static/uploads/contents/zh_hk/dl_centre/monthly/pe/hsi.xls'
path_root = Path(__file__).parent.parent
path1 = os.path.join(path_root, 'data', 'hsi')
Path(path1).mkdir(parents=True, exist_ok=True)

# 2.0 下载pdf
file2 = os.path.join(path1, 'hsi-pe.xls')
if os.path.exists(file2):
    os.remove(file2)
response = requests.get(url)
with open(file2, 'wb') as f:
    f.write(response.content)

# 3.0
wps = win32com.client.Dispatch("ket.Application")
wps.Visible = False
sleep(5)
wb = wps.Workbooks.Open(file2)
data3 = wb.Worksheets('HSI')

# 4.0
names = []
for i in range(2, 6):
    names.append(data3.Cells(3, i).Value)
# 4.1
df4 = pd.DataFrame(columns=['date']+names)
i = 4
date4 = data3.Cells(i, 1).Value
while date4:
    date4 = data3.Cells(i, 1).Value
    date4_1 = str(date4).rstrip("+00:00").rstrip()
    if not date4_1 == 'None':
        date4_2 = datetime.strptime(date4_1, '%Y-%m-%d')
        data4_3 = data3.Cells(i, 2).Value
        data4_4 = data3.Cells(i, 3).Value
        data4_5 = data3.Cells(i, 4).Value
        data4_6 = data3.Cells(i, 5).Value
        data4_7 = pd.Series([date4_2.date(), data4_3, data4_4, data4_5, data4_6], index=['date']+names)
        df4 = df4.append(data4_7, ignore_index=True)
        i = i + 1
    else:
        break
file4 = os.path.join(path1, 'hsi-pe-2.csv')
if os.path.exists(file4):
    os.remove(file4)
df4.to_csv(file4)

wb.Close()
wps.Quit()
del wps
