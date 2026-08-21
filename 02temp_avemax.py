import pandas as pd

# 観測地点(緯度の降順)
places = [
    '旭川', '帯広', '室蘭', '函館', '秋田', '盛岡', '仙台', '山形', '新潟', '福島',
    '富山', '長野', '金沢', '宇都宮','前橋','水戸', '熊谷', '福井', '銚子', '東京',
    '甲府', '鳥取', '松江', '横浜', '岐阜', '彦根', '名古屋','京都','静岡','津',
    '神戸', '大阪', '岡山', '広島', '高松', '和歌山','徳島', '下関', '松山', '福岡',
    '佐賀','大分', '熊本', '長崎', '鹿児島'
]

def estim_date(df:pd.DataFrame, temp:int, fn: str):

    df.columns = df.iloc[0]  # 先頭行を列名に設定
    df = df.iloc[1:].reset_index(drop=True)  # 先頭行を削除
    df["年月日"] = pd.to_datetime(df["年月日"])

    # 結果を辞書の形で返す
    result = {pt : [] for pt in places}

    # 観測地点ごとに推定日を確定する
    for pt in places:       
        
        # 年月日と観測地点のデータフレームを抽出
        i = 1
        # 各年の推定日を計算
        for y in range(2014, 2025):
            s = 0
            while(s <= temp and df['年月日'].iloc[i].year == y):
                s += float(df[pt].iloc[i])
                i += 1
                if i >= df.shape[0]:
                    break
            # 地点pt のリストに推定日を追加する
            if s > temp:
                result[pt].append(df['年月日'].iloc[i])
                while i < df.shape[0] and df['年月日'].iloc[i].year == y:
                    i += 1
            else:
                result[pt].append(df['年月日'].iloc[i-1])

    # CSVファイルへ書込む
    pd.DataFrame(result).to_csv(fn, encoding='shift-jis')

                
# 400度(平均気温)/600度(最高気温) 開花推定日の初期化
dfs_ave = pd.DataFrame()
dfs_max = pd.DataFrame()

#   データ整形処理
# 読込み  
df = pd.read_csv("02temp_data.csv", header=None, encoding="shift_jis", skiprows=2)
#  削除する行（2,3,4行目 → 0始まりで 1,2,3）
df = df.drop(index=[1, 2, 3]).reset_index(drop=True)

# ----------------------------------------
# 平均気温
# 1列目 + 6n+2列（2,8,14,...列目）
# 0始まりでは 0列 + 1,7,13,...
# ----------------------------------------
mean_cols = [0] + list(range(1, df.shape[1], 6))
mean_df = df.iloc[:, mean_cols]
mean_df.iloc[0,0] = "年月日"
# 400度開花推定日をCSVファイルへ書出す
estim_date(mean_df, 400, '02day400.csv')

# ----------------------------------------
# 最高気温
# 1列目 + 6n+5列（5,11,17,...列目）
# 0始まりでは 0列 + 4,10,16,...
# ----------------------------------------
max_cols = [0] + list(range(4, df.shape[1], 6))
max_df = df.iloc[:, max_cols]
max_df.iloc[0,0] = "年月日"
# 600度開花推定日をCSVファイルへ書出す
estim_date(max_df, 600, '02day600.csv')
