import os
import json
import pandas as pd
import numpy as np
from os import walk
from pathlib import Path


# 1.0
path_root = Path(__file__).parent.parent
static_folder = os.path.join(path_root, 'data', 'yieldbook', 'factsheet_daily_usd')
dirs = [name for name in os.listdir(static_folder)]
dirs.remove('tmp')
dirs.remove('html')


# 2.0
data = {}
for dir2 in dirs:
    for root, dirs, files in walk(os.path.join(static_folder, dir2)):
        for file in files:
            filename = file.replace('.csv', '')
            data[filename] = pd.read_csv(os.path.join(static_folder, dir2, file))


# 3.0
data3 = {}
for k3, df3 in data.items():
    # 3.1
    name3 = df3.iloc[1:, 0].values.tolist()
    # 3.2
    for i in range(1, df3.shape[0]):
        tmp3 = df3.iloc[i].values.tolist()
        tem3_1 = tmp3[0]
        tmp3[0] = k3
        # 3.3
        if tem3_1 not in data3:
            columns = ['Date', '当地货币(Index)', '当地货币(Daily)', '当地货币(MTD)', '非对冲 (Index)', '非对冲 (Daily)', '非对冲 (MTD)', '对冲 (Index)', '对冲 (Daily)', '对冲 (Index)']
            data3[tem3_1] = pd.DataFrame(columns=columns)
        data3[tem3_1] = data3[tem3_1].append(pd.Series(tmp3, index=columns), ignore_index=True)


# 4.0
html4_1 = ''
for k4, df4 in data3.items():
    html4_1 += '<h6>'+k4+'</h6>'
    html4_1 += df4.to_html(classes='table table-sm table-striped', index=False, escape=False, border=0, justify='left')
    html4_1 += '<br />'

htm4 = """
<html>
<head>
<meta charset="UTF-8">
<title>富时罗素债券指数-1</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
<script src="https://cdn.datatables.net/1.10.22/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.22/js/dataTables.bootstrap4.min.js"></script>

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
<link rel="stylesheet" href="https://chankuang2008.github.io/kuang-style/css/kuang-style.css" crossorigin="anonymous">
<link rel="stylesheet" href="https://cdn.datatables.net/1.10.22/css/dataTables.bootstrap4.min.css">
<style>
body {font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji","SimHei", "PMingLiU", "Helvetica", "sans-serif";}
.dataframe {font-size: 13px;}
.dataframe th:nth-child(1), .dataframe th:nth-child(4), .dataframe th:nth-child(7),
.dataframe td:nth-child(1), .dataframe td:nth-child(4), .dataframe td:nth-child(7) {
  border-right: 1px solid #cbced2;
}
</style>
<script>

</script>
</head>
<body>

<div class="container">
<div class="row">
<div class="col-12 col-sm-12">
<div class="body-container">
"""+html4_1.replace('NaN', '')+"""
</div>
</div>
</div>
</div>

</body>
</html>
"""

# 5.0
path5 = os.path.join(static_folder, 'html')
Path(path5).mkdir(parents=True, exist_ok=True)
path6 = os.path.join(path5, 'index-1.html')
writer3 = open(path6, "w", encoding="utf-8")
writer3.write(htm4)
writer3.close()
