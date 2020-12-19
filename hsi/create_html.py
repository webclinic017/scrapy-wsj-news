import os
import json
import pandas as pd
import numpy as np
import datetime as dt
from os import walk
from pathlib import Path
from datetime import datetime
from scipy import stats


# 1.0
path_root = Path(__file__).parent.parent
static_folder = os.path.join(path_root, 'data', 'hsi')


# 2.0
file2 = os.path.join(static_folder, 'hsi-pe-2.csv')
df2 = pd.read_csv(file2)
df2['date'] = pd.to_datetime(df2['date'])
names = df2.columns.values.tolist()


# 3.0
columns = ['year', 'nobs', 'min', 'q5%', 'q25%', 'q50%', 'q75%', 'q95%', 'max', 'mean', 'sd', 'variance', 'skewness', 'kurtosis']
df3_1 = pd.DataFrame(columns=columns)
df3_4 = pd.DataFrame(columns=columns)
date3_1 = df2.iloc[-1]['date'].year
date3_2 = df2.iloc[0]['date'].year
for i in range(0, 11):
    def compute(df3_3, name3, title3):
        df3_3 = df3_3[name3]
        stats3 = stats.describe(df3_3.values)
        result3 = df3_3.quantile([.5, .25, .5, .75, .95]).values.tolist()

        data3 = {}
        data3['year'] = title3
        data3['nobs'] = stats3.nobs
        data3['min'] = stats3.minmax[0]
        quan = ['q5%', 'q25%', 'q50%', 'q75%', 'q95%']
        for j in range(len(result3)):
            data3[quan[j]] = result3[j]
        data3['max'] = stats3.minmax[1]
        data3['mean'] = stats3.mean
        data3['sd'] = np.std(df3_3.values)
        data3['variance'] = stats3.variance
        data3['skewness'] = stats3.skewness
        data3['kurtosis'] = stats3.kurtosis
        return data3

    pre_year = dt.date(int(date3_1)-i, 1, 1)
    df3_2 = df2.loc[(df2['date'].dt.date >= pre_year)]
    df3_1 = df3_1.append(compute(df3_2, names[1], str(pre_year.year)+'年起'), ignore_index=True)

    pre_year2 = dt.date(int(date3_1)-i+1, 1, 1)
    mask3 = ((df2['date'].dt.date >= pre_year) & (df2['date'].dt.date <= pre_year2))
    df3_5 = df2.loc[mask3]
    # print(df3_5.shape, df3_5.iloc[0].date, df3_5.iloc[-1].date)
    df3_4 = df3_4.append(compute(df3_5, names[1], str(pre_year.year)+'间'), ignore_index=True)

df3_1.index = df3_1['year']
df3_1.drop(['year'], axis=1, inplace=True)
df3_1 = df3_1.round(3)

df3_4.index = df3_4['year']
df3_4.drop(['year'], axis=1, inplace=True)
df3_4 = df3_4.round(3)

# 4.0
data4_1 = {}
for k4, v4 in df3_1.iterrows():
    data4_1[k4] = v4
df4_1 = pd.DataFrame(data=data4_1)
html4_1 = df4_1.to_html(classes='table table-sm table-striped', escape=False, border=0, justify='left')

data4_2 = {}
for k4, v4 in df3_4.iterrows():
    data4_2[k4] = v4
df4_2 = pd.DataFrame(data=data4_2)
html4_2 = df4_2.to_html(classes='table table-sm table-striped', escape=False, border=0, justify='left')

# 4.1
last = df2.iloc[-1][names[1]]

path4 = os.path.join(static_folder, 'hsi-pe.html')
if os.path.exists(path4):
    os.remove(path4)

htm4 = """
<html>
<head>
<meta charset="UTF-8">
<title>恒生指数市盈率-1</title>
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
</style>
<script>
$(document).ready(function() {

  var colHide = [7, 8, 9, 10, 11, 12];
  for (var noCol of colHide) {
      var th = $(".dataframe tr th:nth-child("+noCol+")");
      th.addClass("d-none").addClass("d-md-table-cell");

      var td = $(".dataframe tr td:nth-child("+noCol+")");
      td.addClass("d-none").addClass("d-md-table-cell");
  }
});
</script>
</head>
<body>
<div class="container">



<div class="row">
<div class="col-12 col-sm-12">
<div class="body-container">
目前市盈率： """ + str(last) + """ <br />
""" + html4_1.replace('NaN', '') + """
</div>
</div>
</div>


<div class="row">
<div class="col-12 col-sm-12">
<div class="body-container">
""" + html4_2.replace('NaN', '') + """
</div>
</div>
</div>



</div>
</body>
</html>
"""

# 5.0
writer3 = open(path4, "w", encoding="utf-8")
writer3.write(htm4)
writer3.close()
