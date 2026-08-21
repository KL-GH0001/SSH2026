import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV読込
df = pd.read_csv("01sakura_bloom_dates.csv", header=0,
                 encoding="utf-8", dtype=str)

# 先頭行から年ラベルを取得
years = df.iloc[:, 0]

counts = []

# 各年について4/1より前に開花した地点数をカウント
for row in range(0, df.shape[0]):
    # 各地点の開花日をリスト
    dates = pd.to_datetime(df.iloc[row, 1:], errors="coerce")
    # 4/1以前の開花日を数える
    count = ((dates.dt.month < 4) |
             ((dates.dt.month == 4) & (dates.dt.day < 1))).sum()
    # 年ごとに集計する
    counts.append(count)

# 年を数値に変換
x = np.array(years.astype(float))
y = np.array(counts)

# 線形回帰
coef = np.polyfit(x, y, 1)      # 傾き・切片
trend = np.poly1d(coef)         # y座標

# 可視化
plt.figure(figsize=(12, 6))

# 元データ
plt.plot(x, y,
         marker="o",
         label="Number of locations blooming before Apr 1")

# 回帰直線（赤）
plt.plot(x, trend(x),
         color="red",
         linewidth=2,
         label=f"Linear trend (slope={coef[0]:.2f})")

plt.ylim(0, 50)
plt.xlabel("Year")
plt.ylabel("Number of locations")
plt.title("Locations with Cherry Blossom Blooming Before April 1")
plt.legend()
plt.grid(True)

# 年が多いので間引いて表示
plt.xticks(x[::5], rotation=45)

plt.tight_layout()
plt.show()