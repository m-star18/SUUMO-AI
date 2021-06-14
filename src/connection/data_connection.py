import pandas as pd
import numpy as np

df = pd.read_csv('../data/suumo_toyotashi.csv', sep='\t', encoding='utf-16')

# 不要な列を削除
df.drop(['Unnamed: 0'], axis=1, inplace=True)

# 立地を「最寄駅」と「徒歩〜分」に分割
splitted1 = df['立地1'].str.split(' 歩', expand=True)
splitted1.columns = ['立地11', '立地12']
splitted2 = df['立地2'].str.split(' 歩', expand=True)
splitted2.columns = ['立地21', '立地22']
splitted3 = df['立地3'].str.split(' 歩', expand=True)
splitted3.columns = ['立地31', '立地32']

# 分割したカラムを結合
df = pd.concat([df, splitted1, splitted2, splitted3], axis=1)

# 分割前のカラムは分析に使用しないので削除しておく
df.drop(['立地1', '立地2', '立地3'], axis=1, inplace=True)

# 「賃料」がNAの行を削除
df = df.dropna(subset=['賃料'])

# エンコードをcp932に変更しておく（これをしないと、replaceできない）
df['賃料'].str.encode('cp932')
df['敷金'].str.encode('cp932')
df['礼金'].str.encode('cp932')
df['管理費'].str.encode('cp932')
df['築年数'].str.encode('cp932')
df['専有面積'].str.encode('cp932')
df['立地12'].str.encode('cp932')
df['立地22'].str.encode('cp932')
df['立地32'].str.encode('cp932')

# 数値として扱いたいので、不要な文字列を削除
df['賃料'] = df['賃料'].str.replace(u'万円', u'')
df['敷金'] = df['敷金'].str.replace(u'万円', u'')
df['礼金'] = df['礼金'].str.replace(u'万円', u'')
df['管理費'] = df['管理費'].str.replace(u'円', u'')
df['築年数'] = df['築年数'].str.replace(u'新築', u'0')  # 新築は築年数0年とする
df['築年数'] = df['築年数'].str.replace(u'築', u'')
df['築年数'] = df['築年数'].str.replace(u'年', u'')
df['専有面積'] = df['専有面積'].str.replace(u'm', u'')
df['立地12'] = df['立地12'].str.replace(u'分', u'')
df['立地22'] = df['立地22'].str.replace(u'分', u'')
df['立地32'] = df['立地32'].str.replace(u'分', u'')

# 「-」を0に変換
df['管理費'] = df['管理費'].replace('-', 0)
df['敷金'] = df['敷金'].replace('-', 0)
df['礼金'] = df['礼金'].replace('-', 0)

# 文字列から数値に変換
df['賃料'] = pd.to_numeric(df['賃料'])
df['管理費'] = pd.to_numeric(df['管理費'])
df['敷金'] = pd.to_numeric(df['敷金'])
df['礼金'] = pd.to_numeric(df['礼金'])
df['築年数'] = pd.to_numeric(df['築年数'])
df['専有面積'] = pd.to_numeric(df['専有面積'])
df['立地12'] = pd.to_numeric(df['立地12'])
df['立地22'] = pd.to_numeric(df['立地22'])
df['立地32'] = pd.to_numeric(df['立地32'])

# 単位を合わせるために、管理費以外を10000倍。
df['賃料'] = df['賃料'] * 10000
df['敷金'] = df['敷金'] * 10000
df['礼金'] = df['礼金'] * 10000

# 管理費は実質的には賃料と同じく毎月支払うことになるため、「賃料+管理費」を家賃を見る指標とする
df['賃料+管理費'] = df['賃料'] + df['管理費']

# 敷金/礼金と保証金は同じく初期費用であり、どちらかが適用されるため、合計を初期費用を見る指標とする
df['敷/礼'] = df['敷金'] + df['礼金']

# 住所を「東京都」「〜区」「市町村番地」に分割
splitted6 = df['住所'].str.split('市', 1, expand=True)
splitted6.columns = ['市', '町']
splitted6['市'] = splitted6['市'] + '市'
splitted6['市'] = splitted6['市'].str.replace('愛知県', '')

# 立地を「路線」「駅」「徒歩〜分」に分割
splitted7 = df['立地11'].str.split('/', expand=True)
splitted7.columns = ['路線1', '駅1']
splitted7['徒歩1'] = df['立地12']
splitted8 = df['立地21'].str.split('/', expand=True)
splitted8.columns = ['路線2', '駅2']
splitted8['徒歩2'] = df['立地22']
splitted9 = df['立地31'].str.split('/', expand=True)
splitted9.columns = ['路線3', '駅3']
splitted9['徒歩3'] = df['立地32']

# 結合
df = pd.concat([df, splitted6, splitted7, splitted8, splitted9], axis=1)

# 不要なカラムを削除
df.drop(['立地11', '立地12', '立地21', '立地22', '立地31', '立地32'], axis=1, inplace=True)

# 階を数値化。地下はマイナスとして扱う
splitted10 = df['階'].str.split('-', expand=True)
splitted10.columns = ['階1', '階2']
splitted10['階1'].str.encode('cp932')
splitted10['階1'] = splitted10['階1'].str.replace(u'階', u'')
splitted10['階1'] = splitted10['階1'].str.replace(u'B', u'-')
splitted10['階1'] = pd.to_numeric(splitted10['階1'])
df = pd.concat([df, splitted10], axis=1)

# 建物高さを数値化。地下は無視。
df['建物高さ'].str.encode('cp932')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下1地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下2地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下3地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下4地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下5地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下6地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下7地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下8地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'地下9地上', u'')
df['建物高さ'] = df['建物高さ'].str.replace(u'平屋', u'1')
df['建物高さ'] = df['建物高さ'].str.replace(u'階建', u'')
df['建物高さ'] = pd.to_numeric(df['建物高さ'])

# indexを振り直す（これをしないと、以下の処理でエラーが出る）
df = df.reset_index(drop=True)

# 間取りを「部屋数」「DK有無」「K有無」「L有無」「S有無」に分割
plans = ['DK', 'K', 'L', 'S']

for plan in plans:
    df[f'間取り{plan}'] = 0
df['間取り'].str.encode('cp932')
df['間取り'] = df['間取り'].str.replace(u'ワンルーム', u'1')

for plan in plans:
    for x in range(len(df)):
        if 'DK' in df['間取り'][x]:
            df.loc[x, f'間取り{plan}'] = 1
    df['間取り'] = df['間取り'].str.replace(u'{0}'.format(plan), u'')

df['間取り'] = pd.to_numeric(df['間取り'])

# カラムを入れ替えて、csvファイルとして出力
df = df[['マンション名', '住所', '市', '町', '間取り', '間取りDK', '間取りK', '間取りL', '間取りS', '築年数', '建物高さ', '階1', '専有面積',
         '賃料+管理費', '敷/礼', '路線1', '駅1', '徒歩1', '路線2', '駅2', '徒歩2', '路線3', '駅3', '徒歩3', '賃料', '管理費', '敷金', '礼金']]

df.to_csv('suumo_toyotashi1.csv', sep='\t', encoding='utf-16')
