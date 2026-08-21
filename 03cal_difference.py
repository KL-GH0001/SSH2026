import pandas as pd

# 読み込み
bloom = pd.read_csv("01sakura_bloom_dates.csv", encoding="shift-jis")
d600 = pd.read_csv("02day600.csv", encoding="shift-jis")
d400 = pd.read_csv("02day400.csv", encoding="shift-jis")

# bloom: 年をインデックス化
bloom = bloom.set_index("地点名")

# day600, day400: 行番号を年に変換
years = bloom.index.astype(int)

d600.index = years
d400.index = years

# 日付型へ変換
bloom = bloom.apply(pd.to_datetime)
d600 = d600.apply(pd.to_datetime)
d400 = d400.apply(pd.to_datetime)

# 列名の空白除去
bloom.columns = bloom.columns.str.strip()
d600.columns = d600.columns.str.strip()
d400.columns = d400.columns.str.strip()

# 列順を bloom に合わせる
d600 = d600[bloom.columns]
d400 = d400[bloom.columns]

# 日数差計算
diff600 = (d600 - bloom).apply(lambda x: x.dt.days)
diff400 = (d400 - bloom).apply(lambda x: x.dt.days)

# 保存
diff600.to_csv("03_600diff.csv", encoding="shift_jis")
diff400.to_csv("03_400diff.csv", encoding="shift_jis")



