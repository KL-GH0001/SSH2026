# ------------------------------------------------------------------------------
# 01．  気象庁のオープンデータから全国の観測地点におけるさくらの開花日データを取得
#       データクリーニングと取得
#       CSVファイルへ書込む
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# (01-01) Shift-JIS形式のCSVファイルを読込む
df = pd.read_csv(
    "01sakura.csv",         # CSVファイル名
    header=None,            # すべての行をデータとみなす
    encoding="shift_jis",   # 文字コード形式
    dtype=str,              # データタイプ
    skiprows=1              # 先頭行を削除
)

# --------------------------------------
# (01-02) データクリーニングとデータ整形

# A列～ER列のうち、A列(0)～EO列(144)の偶数列を抽出
df = df.iloc[:, :145] 
# 列のいずれかに "0" が含まれる行を削除
df = df[~(df == "0").any(axis=1)]
# DU列(124)～EO列(144)の偶数列を抽出
df_cleaned = pd.concat([df.iloc[:,1], df.iloc[:, 124:145:2]], axis=1).copy()
# df_cleaned= df_cleaned.reset_index(drop=True)
# df_cleaned.columns = range(len(df_cleaned.columns))
# print(df_cleaned.head())

# 整数 → 年月日に変換
for col in range(1, df_cleaned.shape[1]):
    year = int(df_cleaned.iloc[0, col])
    print(year)
    df_cleaned.iloc[1:, col] = df_cleaned.iloc[1:, col].apply(
        lambda x: pd.Timestamp(
            year=year,
            month=int(x)//100,
            day=int(x)%100
        )
    )

# 行方向に年を，列方向に地点を並べる
df_cleaned = df_cleaned.transpose()

# --------------------------------------
# (01-03) Shift-JIS形式のCSVファイルで保存

df_cleaned.to_csv(
    "01sakura_bloom_dates.csv",
    index=False,                # 1列目に通し番号を付加しない
    header=False,               # 1行目に通し番号を付加しない              
#    encoding="shift_jis",
    encoding="utf-8-sig",
)

# 報告
print("データクリーニング完了")


# --------------------------------------
# (01-04) 折れ線グラフの描画

# 先頭行から年ラベルを取得
years = df_cleaned.iloc[1:, 0]

# 日数(y座標)のリスト初期化
counts = []

# 各年について4/1より前に開花した地点数をカウント
for row in range(1, df_cleaned.shape[0]):
    # 各地点の開花日をリスト
    dates = pd.to_datetime(df_cleaned.iloc[row, 1:], errors="coerce")
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


