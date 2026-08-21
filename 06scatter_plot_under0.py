# ------------------------------------------------------------------------------
# 06．氷点下(subzero temperature)日数と400度開花差の散布図と回帰直線
#
#
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# (06.01) 観測地点(緯度の降順)リスト
places = [
    '旭川', '帯広', '室蘭', '函館', '秋田', '盛岡', '仙台', '山形', '新潟', '福島',
    '富山', '長野', '金沢', '宇都宮','前橋','水戸', '熊谷', '福井', '銚子', '東京',
    '甲府', '鳥取', '松江', '横浜', '岐阜', '彦根', '名古屋','京都','静岡','津',
    '神戸', '大阪', '岡山', '広島', '高松', '和歌山','徳島', '下関', '松山', '福岡',
    '佐賀','大分', '熊本', '長崎', '鹿児島'
]
               
#  (06.02)．気温データ整形処理
#
#  気温データの読込み  
df = pd.read_csv("02temp_data.csv", header=None, encoding="shift_jis", skiprows=2)
#  削除する行（2,3,4行目 → 0始まりで 1,2,3）
df = df.drop(index=[1, 2, 3]).reset_index(drop=True)

#  先頭(0)行は列名として使う．縦方向のインデックスを振り直し
df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

#  平均気温の抽出，0列を日付型へ変換, 1列以降はfloat型へ変換
#   1列目 + 6n+2列（2,8,14,...列目）0始まりでは 0列 + 1,7,13,...
mean_cols = [0] + list(range(1, df.shape[1], 6))
mean_df = df.iloc[:, mean_cols].copy()
mean_df.iloc[:, 0] = pd.to_datetime(mean_df.iloc[:, 0])
mean_df.iloc[:, 1:] = mean_df.iloc[:, 1:].apply(pd.to_numeric)
print(mean_df.dtypes)

#  最新3年分の平均気温を抽出，地点・年度毎に平均気温が氷点下(0度以下)の日数を求める
mean_df_2022 = mean_df[(pd.to_datetime(mean_df.iloc[:, 0]).dt.year == 2022)]
X = [mean_df_2022[mean_df_2022[pt].iloc[:] <= 0].shape[0] for pt in places]
mean_df_2023 = mean_df[(pd.to_datetime(mean_df.iloc[:, 0]).dt.year == 2023)]
X += [mean_df_2023[mean_df_2023[pt].iloc[:] <= 0].shape[0] for pt in places]
mean_df_2024 = mean_df[(pd.to_datetime(mean_df.iloc[:, 0]).dt.year == 2024)]
X += [mean_df_2024[mean_df_2024[pt].iloc[:] <= 0].shape[0] for pt in places]
X = np.array(X)
print(X)

# 
# days_U0 = [mean_df_2022_24[mean_df_2022_24[pt].iloc[:] <= 0].shape[0] for pt in places]
# print(days_U0)

# (06.03) 400度開花差データの整形処理
df400 = pd.read_csv("03_400diff.csv", header=0, encoding='shift-jis')
# 地点毎に最近3年の400度開花差日数を求める
Y = [df400[pt].iloc[8] for pt in places]
Y += [df400[pt].iloc[9] for pt in places]
Y += [df400[pt].iloc[10] for pt in places]
Y = np.array(Y)
print(Y)

# (06.04) 散布図と回帰直線
# 散布図
plt.scatter(X, Y)

# 回帰直線
a, b = np.polyfit(X, Y, 1)
plt.plot(X, a*X + b, color="red")

# 回帰式を表示
plt.text(
    0.05, 0.95,
    f"y = {a:.3f}x + {b:.3f}",
    transform=plt.gca().transAxes,
    verticalalignment="top"
)

# 軸ラベル
plt.xlabel("氷点下日数")
plt.ylabel("開花差")
# タイトル
plt.title("図3 氷点下日数と400度開花差の散布図")

plt.show()

