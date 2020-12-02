import os
import json
import pandas as pd
from os import walk
from pathlib import Path

path_root = Path(__file__).parent.parent.parent
static_folder = os.path.join(path_root, 'data', 'wsj')
dirs = [name for name in os.listdir(static_folder)]
dirs.remove('html')
data = []

for dir2 in dirs:
    for root, dirs, files in walk(os.path.join(static_folder, dir2, 'json')):
        for file in files:
            with open(os.path.join(root, file), encoding="utf-8") as json_file:
                data.append(json.load(json_file))

df1 = pd.DataFrame(data)
df1['time'] = pd.to_datetime(df1['time'])
df1 = df1.sort_values(by='time', ascending=False)
df1['title_2'] = '<a target="_blank" href="'+df1['url_original']+'">'+df1['title']+'</a>'
df1['date'] = df1['time'].dt.strftime('%Y-%m')
df1['image_2'] = '<img src="../'+df1['date']+'/img/'+df1['image_1']+'">'

# index-2
df2 = df1.copy(deep=True)
df2 = df2[['time', 'category_1', 'title_2', 'sub_head', 'body', 'image_2']]
df2.columns = ['时间', '分类', '标题', '副标题', '正文', '图片']
df2 = df2.head(100)
path_output2 = os.path.join(path_root, 'data', 'wsj', 'html', 'index-2.html')
html2 = df2.to_html(classes='table table-sm table-striped', border=0, escape=False, index=False)
html2_1 = """
<html>
<head>
<meta charset="UTF-8">
<title>华尔街日报爬虫-2</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>


<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
<link rel="stylesheet" href="https://chankuang2008.github.io/kuang-style/css/kuang-style.css">
<style>
body {font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji","SimHei", "PMingLiU", "Helvetica", "sans-serif";}
.dataframe {font-size: 13px;}
.dataframe td:nth-child(1) {width: 8%;}
.dataframe td:nth-child(3) {width: 15%;}
.dataframe td:nth-child(5) {width: 40%;}
</style>
</head>
<body>

<div class="container">
<div class="row">
<div class="col-12 col-sm-12">
<div class="body-container">
"""+html2.replace('NaN', '')+"""
</div>
</div>
</div>
</div>

</body>
</html>
"""
writer2 = open(path_output2, "w", encoding="utf-8")
writer2.write(html2_1)
writer2.close()

# index-1
df3 = df1.copy(deep=True)
df3 = df3[['time', 'category_1', 'title_2', 'sub_head', 'image_2']]
df3.columns = ['时间', '分类', '标题', '副标题', '图片']
path_output3 = os.path.join(path_root, 'data', 'wsj', 'html', 'index-1.html')
html3 = df3.to_html(classes='table table-sm table-striped', border=0, escape=False, index=False)
html3_1 = """
<html>
<head>
<meta charset="UTF-8">
<title>华尔街日报爬虫-1</title>
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
.dataframe td:nth-child(1) {width: 10%;}
.dataframe td:nth-child(2) {width: 10%;}
.dataframe td:nth-child(3) {width: 30%;}
.dataframe td:nth-child(4) {width: 40%;}
.dataframe td:nth-child(5) {width: 10%;}
.dataTables_info, .form-control-sm, label, .paginate_button {font-size: 12px;}
</style>
<script>
$(document).ready(function() {
  var th1 = $(".dataframe tr th:nth-child(1)");
  th1.addClass("d-none").addClass("d-md-table-cell");
  
  var td1 = $(".dataframe tr td:nth-child(1)");
  td1.addClass("d-none").addClass("d-md-table-cell");
  
  var th5 = $(".dataframe tr th:nth-child(5)");
  th5.addClass("d-none").addClass("d-md-table-cell");
  
  var td5 = $(".dataframe tr td:nth-child(5)");
  td5.addClass("d-none").addClass("d-md-table-cell");
  
  $('.dataframe').DataTable({
    order: [[0, "desc"]],
    paging: true,
    pageLength: 100
  });
});
</script>
</head>
<body>

<div class="container">
<div class="row">
<div class="col-12 col-sm-12">
<div class="body-container">
"""+html3.replace('NaN', '')+"""
</div>
</div>
</div>
</div>

</body>
</html>
"""
writer3 = open(path_output3, "w", encoding="utf-8")
writer3.write(html3_1)
writer3.close()
