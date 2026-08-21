import pandas as pd

# 観測地点(緯度の降順)
places = [
    '旭川', '帯広', '室蘭', '函館', '秋田', '盛岡', '仙台', '山形', '新潟', '福島',
    '富山', '長野', '金沢', '宇都宮','前橋','水戸', '熊谷', '福井', '銚子', '東京',
    '甲府', '鳥取', '松江', '横浜', '岐阜', '彦根', '名古屋','京都','静岡','津',
    '神戸', '大阪', '岡山', '広島', '高松', '和歌山','徳島', '下関', '松山', '福岡',
    '佐賀','大分', '熊本', '長崎', '鹿児島'
]

               
#   データ整形処理
# 読込み  
df = pd.read_csv("02temp_data.csv", header=None, encoding="shift_jis", skiprows=2)
#  削除する行（2,3,4行目 → 0始まりで 1,2,3）
df = df.drop(index=[1, 2, 3]).reset_index(drop=True)

# 先頭行は列名
df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

# 


# ----------------------------------------
# 平均気温
# 1列目 + 6n+2列（2,8,14,...列目）
# 0始まりでは 0列 + 1,7,13,...
# ----------------------------------------
mean_cols = [0] + list(range(1, df.shape[1], 6))
mean_df = df.iloc[:, mean_cols]

# データを日付型へ変換
mean_df.iloc[:, 0] = pd.to_datetime(mean_df.iloc[:, 0])
mean_df_2024 = mean_df[pd.to_datetime(mean_df.iloc[:, 0]).dt.year == 2024]
mean_df_2024.iloc[:, 1:] = mean_df_2024.iloc[:, 1:].astype(float)
print(mean_df_2024.head())

# 平均気温が氷点下(0度以下)の日があった地点の抽出
G1 = [pt for pt in places if not((mean_df_2024[pt].iloc[1:] > 0).all())]
G2 = [pt for pt in places if (mean_df_2024[pt].iloc[1:] > 0).all()]
# print(G1, G2)

df400 = pd.read_csv("03_400diff.csv", header=0, encoding='shift-jis')
d400_2024_G1 = [int(df400[pt].iloc[10]) for pt in G1]
d400_2024_G2 = [int(df400[pt].iloc[10]) for pt in G2]
print(d400_2024_G1)
print(d400_2024_G2)

# 水平方向の箱ひげ図
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

fig, ax = plt.subplots()

bp = ax.boxplot(
    [d400_2024_G1, d400_2024_G2],
    vert=False,
    patch_artist=True,
    
)

ax.set_yticklabels(['G1', 'G2'])

colors = ["skyblue", "lightgreen"]

for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)

legend_elements = [
    Patch(facecolor="skyblue", label="Group A"),
    Patch(facecolor="lightgreen", label="Group B")
]

ax.legend(handles=legend_elements, title="Group")
plt.show()

