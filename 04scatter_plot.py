import pandas as pd

# 地点と緯度データ
places = {
    "旭川": 43.77,
    "帯広": 42.92,
    "室蘭": 42.32,
    "函館": 41.77,
    "秋田": 39.72,
    "盛岡": 39.70,
    "山形": 38.25,
    "仙台": 38.26,
    "福島": 37.76,
    "新潟": 37.92,
    "金沢": 36.59,
    "富山": 36.70,
    "長野": 36.65,
    "宇都宮": 36.56,
    "福井": 36.07,
    "前橋": 36.39,
    "熊谷": 36.15,
    "水戸": 36.37,
    "岐阜": 35.42,
    "名古屋": 35.18,
    "甲府": 35.67,
    "銚子": 35.73,
    "津": 34.73,
    "静岡": 34.98,
    "東京": 35.69,
    "横浜": 35.44,
    "松江": 35.47,
    "鳥取": 35.50,
    "京都": 35.01,
    "彦根": 35.27,
    "下関": 33.95,
    "広島": 34.39,
    "岡山": 34.66,
    "神戸": 34.69,
    "大阪": 34.69,
    "和歌山": 34.23,
    "福岡": 33.59,
    "佐賀": 33.25,
    "大分": 33.24,
    "長崎": 32.75,
    "熊本": 32.80,
    "鹿児島": 31.56,
    "松山": 33.84,
    "高松": 34.34,
    "徳島": 34.07
}

#
df400 = pd.read_csv("03_400diff.csv", header=0, encoding='shift-jis')
df600 = pd.read_csv("03_600diff.csv", header=0, encoding='shift-jis')

import matplotlib.pyplot as plt

lats = [lat for pt, lat in places.items()]
d400 = [df400[pt].iloc[10] for pt in places.keys()]
d600 = [df600[pt].iloc[10] for pt in places.keys()]

# 散布図
plt.figure(figsize=(8, 6))

# 400日積算: ○
plt.scatter(
    lats, d400,
    marker='o',
    label='400'
)

# 600日積算: ×
plt.scatter(
    lats, d600,
    marker='x',
    label='600'
)

# 相関係数
import numpy as np
x = np.array(lats)
y1 = np.array(d400)
y2 = np.array(d600)

r1 = np.corrcoef(x, y1)[0, 1]
r2 = np.corrcoef(x, y2)[0, 1]

# 相関係数を表示
plt.text(
    0.05, 0.95,
    f"Correl o : r = {r1:.3f}, $R^2$ = {r1 ** 2:.3f}\nCorre; × : r = {r2:.3f}, $R^2$ = {r2 ** 2:.3f}",
    transform=plt.gca().transAxes,
    va="top",
    bbox=dict(
        facecolor="white", # 背景色
        edgecolor="black", # 枠線色
        boxstyle="round", # 枠の形
        alpha=0.8 # 透明度
    )
)

# 軸ラベル
plt.xlabel("Latitude")
plt.ylabel("Days after bloom")
# 凡例
plt.legend()
# グリッド
plt.grid(True)

plt.show()