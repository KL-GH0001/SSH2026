import pandas as pd

# 表形式データ（DataFrame）にする
print(f'----- DataFrame, shape, size, index, colomns -----')
df = pd.DataFrame({
    "名前": ["佐藤", "鈴木", "高橋", "田中", "渡辺"],
    "国語": [80, 95, 64, 95, 0],
    "数学": [7, 100, 50, 90, 10],
    "英語": [7, 100, 50, 93, 15],
})

print(df)
print('■\n',f"df.shape={df.shape}, df.size={df.size}")  # shape: (5,4), size:20
print('■\n',f"df.index={df.index}")                     # [0,1,2,3,4]
print('■\n',f"df.columns={df.columns}")                 # ['名前', '国語', '数学', '英語']

# Series
print(f'----- Series(列) -----')
s = df["名前"]
print(f"Series:\n {s}") # ["佐藤", "鈴木", "高橋", "田中", "渡辺"]

print(f'----- データの抽出 -----')
print('■ df.iloc[0,0]\n', df.iloc[0,0])     # [行番号, 列番号] → 要素 0行0列」
 
print('■ df.iloc[1]\n', df.iloc[1])              # [行番号]           → 1行指定 「1行目」
print('■ df.iloc[[2,4]])\n', df.iloc[[2,4]])     # [行番号, 行番号]   → 列挙 「2行目と4行目」
print('■ df.iloc[0:5:2])\n', df.iloc[0:5:2])     # [行番号:行番号]    → 範囲 「0行から4行の偶数行目」

print('■ df.iloc[:,1]\n', df.iloc[:,1])             # [列番号]           → 1列指定 「1列目」
print('■ df["国語"]\n', df["国語"])               # [列名]             → 1列指定 「1列目」ｑ
# (間違い) print('■ df.loc["国語"]\n', df.loc["国語"])               # [列名]             → 1列指定 「1列目」
print('■ df.iloc[:,[1,3]])\n', df.iloc[[2,4]])      # [列番号, 列番号]   → 列挙 「1列目と3列目」
print('■ df.iloc[0:4:2])\n', df.iloc[0:5:2])        # [列番号: 列番号]   → 範囲 「0列から3列の偶数列目」
 
print("■ df.loc[:,'名前']\n", df.loc[:, '名前'])                            # [列名]           →  列名指定 「名前列」
print("■ df.loc[:,['名前', '数学']])\n", df.loc[:, ['名前','数学']])        # [列名, 列名]   → 列名列挙 「名前列と数学列」

print("■ df.loc[:,'名前']\n", df[df['数学'] > 90])    # 数学が90点を超える行


print(f'----- データの削除 -----')
df = pd.DataFrame({
    "名前": ["佐藤", "鈴木", "高橋", "田中", "渡辺"],
    "国語": [80, 95, 64, 95, 0],
    "数学": [7, 100, 50, 90, 10],
    "英語": [7, 100, 50, 93, 15],
})
  
print("■ df.drop(1)\n", df.drop(1))    # 行の削除したdfのコピーを返す（元のdfは変更されない）
print("■ df.drop([0, 4])\n", df.drop([0, 4]))  # 複数行の削除したdfのコピーを返す（元のdfは変更されない） 

print("■ df.drop('英語', axis=1)\n", df.drop('英語', axis=1))    # 列の削除したdfのコピーを返す（元のdfは変更されない）
print("■ df.drop(['数学','英語'], axis=1)\n", df.drop(['数学','英語'], axis=1))    # 列の削除したdfのコピーを返す（元のdfは変更されない）



print(f'----- データの読込みと書込み -----')
df = pd.DataFrame({
    "名前": ["佐藤", "鈴木", "高橋", "田中", "渡辺"],
    "国語": [80, 95, 64, 95, 0],
    "数学": [7, 100, 50, 90, 10],
    "英語": [8, 100, 50, 93, 15],
})
df.to_csv('00sample.csv') # 1行目は列名, 1列目に行名(行番号)を付加して書出す
df1 = pd.read_csv('00sample.csv') # 1行目は列名, 1列目に行名(行番号)を付加せず読込む
print(df1.dtypes)

df.to_csv('00sample.csv', index=False) # 1行目は列名, 1列目に行名(行番号)を付加せず書き出す
df1 = pd.read_csv('00sample.csv', header=None) # 1行目は列名とみなさず, データとみなす


print(f'----- データの結合 -----')
dfA = pd.DataFrame({
    "名前": ["佐藤", "鈴木", "高橋", "田中", "渡辺"],
    "理科": [41, 45, 44, 45, 40],
    "社会": [57, 50, 54, 52, 55],
})
print(pd.concat([df, dfA], axis=1)) # 横方向, 外部結合，✖ 科目が2列に現れる
print(df.merge(dfA, on='名前')) # 横方向, 名前をキーとして外部結合

print(f'----- transpose -----')
df = pd.DataFrame({
    "名前": ["佐藤", "鈴木", "高橋", "田中", "渡辺"],
    "国語": [80, 95, 64, 95, 0],
    "数学": [7, 100, 50, 90, 10],
    "英語": [7, 100, 50, 93, 15],
})
print(df, df.shape, df.transpose(), df.transpose().shape)