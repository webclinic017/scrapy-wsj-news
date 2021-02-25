import random


def get_random_header():
    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        # Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
    ]
    return {'User-Agent': random.choice(user_agent_list)}


def remove_line(data):
    return "".join(line.strip() for line in data.split("\n"))


def remove_first_end_spaces(data):
    return "".join(data.rstrip().lstrip())


def get_ucodes():
    codes = {
        # 騰訊, 美團, 阿里, 京東, 藍月亮,, 泡泡瑪特, 網易, 快手, 京东健康
        '新經濟': ['0700.HK', '3690.HK', '9988.HK', '9618.HK', '6993.HK', '9992.HK', '9999.HK', '1024.HK', '6618.HK'],
        #
        '指數': ['.HSI', '.DJI', '.SP500', '.NASI', '.SSEC', '.CSI300', '.SZI', '.HSCE'],
        # 中石化, 中海洋, 中石油
        '石油': ['0386.HK', '0883.HK', '0857.HK'],
        # 昆能, 中燃氣, 新奧, 華潤燃氣, 北京控股
        '天然氣': ['0135.HK', '0384.HK', '2688.HK', '1193.HK', '0392.HK'],
        # 神華, 江銅, 鞍鋼, 金隅, 中鋁
        '資源': ['1088.HK', '0358.HK', '0347.HK', '2009.HK', '2600.HK'],
        # 山東黃金, SPDR金ETF, 招金
        '黃金': ['1787.HK', '2840.HK', '1818.HK'],
        # 華泥, 海泥, 中建材, 亞洲水泥, 山水, 聯塑
        '水泥建材': ['1313.HK', '0914.HK', '3323.HK', '0743.HK', '0691.HK', '2128.HK'],
        # 旭輝, 綠城, 保利, 藍光, 雅生活, 碧桂園, 佳兆業, 新城悅
        '物管': ['0884.HK', '3900.HK', '6049.HK', '2606.HK', '3319.HK', '6098.HK', '2168.HK', '1755.HK'],
        # 首創, 富力, 恒大, 碧桂園, 世茂房, 奧園, 華潤, 中海外, 融創, 萬科, 越秀, 雅居樂, 中海外, 龍湖
        '內房': ['2868.HK', '2777.HK', '3333.HK', '2007.HK', '0813.HK', '3883.HK', '1109.HK', '0688.HK', '1918.HK',
               '2202.HK', '0123.HK', '3383.HK', '3311.HK', '0960.HK'],
        # 中銀, 交行, 建行, 工商, 郵儲, 招商, 農行
        '內銀': ['2388.HK', '3328.HK', '0939.HK', '1398.HK', '1658.HK', '3968.HK', '1288.HK'],
        # 平安, 中人壽, 太保, 太平, 新華, 財險, 眾安
        '內險': ['2318.HK', '2628.HK', '2601.HK', '0966.HK', '1336.HK', '2328.HK', '6060.HK'],
        # 特步, 波司登, 安踏, 李寧, 海底撈, 貓眼, 閱文, 同程藝龍, 361, 青啤, 華啤, 旺旺, 呷哺呷哺, 頤海
        '內消': ['1368.HK', '3998.HK', '2020.HK', '2331.HK', '6862.HK', '1896.HK', '0772.HK', '0780.HK', '1361.HK',
               '0169.HK', '0291.HK', '0151.HK', '0520.HK', '1579.HK'],
        # 恆安, 蒙牛, 華啤, 申洲, Ｈ&Ｈ, 裕元, 高鑫, 達利, 國美, 滔搏, 萬洲, 康師傅, 周黑鴨, 飛鶴, 澳優
        '內需': ['1044.HK', '2319.HK', '0291.HK', '2313.HK', '1112.HK', '0551.HK', '6808.HK', '3799.HK', '0493.HK',
               '6110.HK', '0288.HK', '0322.HK', '1458.HK', '6186.HK', '1717.HK'],
        # 中信, 中金, 國君, 華泰, 招商, 廣發, 海通, 光大
        '內商': ['6030.HK', '3908.HK', '2611.HK', '6886.HK', '6099.HK', '1776.HK', '6837.HK', '6178.HK'],
        # 灣區發展, 浙江滬杭甬, 江蘇寧滬高速, 深圳高速, 路勁, 越秀交通, 安徽皖通, 深圳國際, 廣深鐵
        '公路': ['0737.HK', '0576.HK', '0177.HK', '0548.HK', '1098.HK', '1052.HK', '0995.HK', '0152.HK', '0525.HK'],
        # 中交建, 中聯重科
        '基建': ['1800.HK', '1157.HK'],
        # 中鐵, 中鐵建, 通號, 中車, 中車時代電氣
        '鐵路': ['0390.HK', '1186.HK', '3969.HK', '1766.HK', '3898.HK'],
        # 中移, 電信, 聯通, 鐵塔,
        '電訊': ['0941.HK', '0728.HK', '0762.HK', '0788.HK'],
        # 瑞聲, 比迪, 舜宇, 小米, 中芯, 華虹, 中興, 南京熊貓, ASMPACIF
        '5G': ['2018.HK', '1211.HK', '2382.HK', '1810.HK', '0981.HK', '1347.HK', '0763.HK', '0553.HK', '0522.HK'],
        # 京信通信, 南方通信, 中國通信
        '電訊設備': ['2342.HK', '1617.HK', '0552.HK'],
        # 吉利, 比迪, 廣汽, 華晨, 東風, 長城, 北汽, 慶鈴
        '汽車': ['0175.HK', '1211.HK', '2238.HK', '1114.HK', '0489.HK', '2333.HK', '1958.HK', '1122.HK'],
        # 復星, 石藥, 中生, 藥明康德, 信達, 翰森, 康龍化成, 白雲山, 國藥, 東陽
        '醫藥': ['2196.HK', '1093.HK', '1177.HK', '2359.HK', '1801.HK', '2269.HK', '3692.HK', '3759.HK', '0874.HK',
               '1099.HK', '1558.HK'],
        # 平安好醫生, 阿里健康, 微創醫療, 錦欣生殖, 威高, 春立, 金斯瑞, 康希諾, 諾輝健康
        '新醫療': ['1833.HK', '0241.HK', '0853.HK', '1951.HK', '1066.HK', '1858.HK', '1548.HK', '6185.HK', '6606.HK'],
        # 匯控, 中行, 渣打, 恆生
        '本地銀行': ['0005.HK', '3988.HK', '2888.HK', '0011.HK'],
        # 電盈, 數碼通,
        '本地電訊': ['0008.HK', '0315.HK'],
        # 電能, 中電, 領展, 港鐵, 煤氣, 港燈
        '本地必需': ['0006.HK', '0002.HK', '0823.HK', '0066.HK', '0003.HK', '2638.HK'],
        # 新鴻基, 長實, 恒基, 信和, 新世界
        '藍籌地產': ['0016.HK', '1113.HK', '0012.HK', '0083.HK', '0017.HK'],
        # 新世界, 九倉, 龍光, 信和, 華地, 恆隆, 新鴻基, 恆基, 太古, 長建, 長和, 太古
        '本地房建': ['0017.HK', '1997.HK', '3380.HK', '0083.HK', '1700.HK', '0101.HK', '0016.HK', '0012.HK', '0019.HK',
                 '1038.HK', '0001.HK', '0019.HK'],
        # 置富, 越秀, 陽光, 冠君, 睿富, 招商, 春泉, 泓富
        '本地物管': ['0778.HK', '0405.HK', '0435.HK', '2778.HK', '0625.HK', '1503.HK', '1426.HK', '0808.HK'],
        # 港交
        '證商': ['0388.HK'],
        # 友邦, 宏利, 保誠
        '保險': ['1299.HK', '0945.HK', '2378.HK'],
        # 銀河, 金沙, 永利, 金界, 美高梅, 澳博
        '博彩': ['0027.HK', '1928.HK', '1128.HK', '3918.HK', '2282.HK', '0880.HK'],
        # 百威, 優品, 永安, 利福, 永旺, 金鷹, 利亞, 維他奶
        '消費零售': ['1876.HK', '2360.HK', '0289.HK', '1212.HK', '0984.HK', '3308.HK', '0831.HK', '0345.HK'],
        # 國泰, 國航, 南航, 東航, 中銀航空租賃
        '航空': ['0293.HK', '0753.HK', '1055.HK', '0670.HK', '2588.HK'],
        # 微盟, 金山
        '科技': ['2013.HK', '3888.HK'],
        # 海螺創業, 創科實業
        '實業': ['0586.HK', '0669.HK'],
        # 華夏滬深300, 領航標普500, 盈富, 恒指ETF, 安碩恒生指數, 安碩A50, 南方A50, 安碩滬深300, 南方恒生科技
        '指數ETF': ['3188.HK', '9140.HK', '2800.HK', '2833.HK', '3115.HK', '2823.HK', '2822.HK', '2846.HK', '3033.HK'],
        # 南方恒指+2x, 華夏納一百+2x, 華夏恆指+2x
        "指數ETFx": ['7200.HK', '7261.HK', '7221.HK'],
        # 南方恒指-1x, 南方納指-2x, 華夏納一百-2x, 華夏納一百-1x
        "反向指數ETFx": ['7500.HK', '7568.HK', '7522.HK', '7331.HK'],
        # 網易, 陌陌, 京東, 拼多多, 搜狐, 百度, 新浪, 迅雷, 微博, 阿里巴巴, 獵豹移動, 百胜中国
        '中概美股': ['NTES.O', 'MOMO.O', 'JD.O', 'PDD.O', 'SOHU.O', 'BIDU.O', 'SINA.O', 'XNET.O', 'WB.O',
                 'BABA.K', 'CMCM.K', 'YUMC.K']
    }
    return codes
