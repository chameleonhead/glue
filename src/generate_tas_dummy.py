import pandas as pd
import numpy as np
from faker import Factory
import os.path
import datetime

# create some fake data
fake = Factory.create('ja_JP')


def make_kyouhanten(num):
    return [{'共販店コード': x+1000, '共販店名': fake.company()} for x in range(num)]


def make_kyoten(num):
    return [{'拠点コード': x+1000, '拠点名': fake.administrative_unit() + fake.city()} for x in range(num)]


def make_hinban(num):
    return [{'品番': x+1000, '品名': fake.color_name()} for x in range(num)]


def make_okyakusama(num):
    return [{'お客様コード': x+1000, 'お客様名': fake.company()} for x in range(num)]


def make_shimukesaki(num):
    return [{'仕向先コード': x+1000, '仕向先名': fake.company()} for x in range(num)]


def make_make(num):
    return [{'メーカーコード': x+1000, 'メーカー名': fake.company()} for x in range(num)]


def load_or_create_csv(fname, factory, num):
    if os.path.isfile(fname):
        return pd.read_csv(fname)
    else:
        df = pd.DataFrame(factory(num=num))
        df.to_csv(fname, index=False)
        return df


kyouhanten_df = load_or_create_csv(
    'data/tas/kyouhanten.csv', make_kyouhanten, 100)
kyoten_df = load_or_create_csv('data/tas/kyoten.csv', make_kyoten, 100)
hinban_df = load_or_create_csv('data/tas/hinban.csv', make_hinban, 100)
okyakusama_df = load_or_create_csv(
    'data/tas/okyakusama.csv', make_okyakusama, 100)
shimukesaki_df = load_or_create_csv(
    'data/tas/shimukesaki.csv', make_shimukesaki, 100)
make_df = load_or_create_csv('data/tas/make.csv', make_make, 100)


def make_orders(kyouhanten_code, juchu_kyoten_code, date, num):

    hinban_list = hinban_df['品番'].tolist()

    fake_orders = [{'共販店コード': kyouhanten_code,
                    '受注拠点コード': juchu_kyoten_code,
                    '受注日': date,
                    'アイテムNo.': item_no,
                    '品番': np.random.choice(hinban_list)} for item_no in range(1, 1 + num)]

    return fake_orders


def make_nouki_shitei_file(kyouhanten_code, okyakusama_code, date, num):

    hinban_list = hinban_df['品番'].tolist()
    maker_kbn_list = ['自社生産', '仕入れ']

    fake_orders = [{'共販店コード': kyouhanten_code,
                    'お客様コード': okyakusama_code,
                    '品番': np.random.choice(hinban_list),
                    'メーカー区分': np.random.choice(maker_kbn_list),
                    '入庫拠点': np.random.choice(maker_kbn_list),
                    '注文No.': order_no,
                    '納期指定日': date} for order_no in range(1, 1 + num)]

    return fake_orders


def make_nouhin(kyouhanten_code, shimukesaki_code, make_code, date, num):

    hinban_list = hinban_df['品番'].tolist()

    fake_orders = [{'共販店コード': kyouhanten_code,
                    '仕向先コード': shimukesaki_code,
                    'メーカーコード': make_code,
                    'イシュNo.': order_no,
                    'イシュ内連番': 1,
                    '品番': np.random.choice(hinban_list),
                    'メーカー出荷日': fake.date_between(start_date=date, end_date='+10'),
                    '入庫入力日': fake.date_between(start_date=date, end_date='+10')} for order_no in range(1, 1 + num)]

    return fake_orders


print(kyouhanten_df.head())
print(kyoten_df.head())
print(hinban_df.head())
print(shimukesaki_df.head())
print(make_df.head())

today = datetime.date.today()
date_list = [today + datetime.timedelta(days=num) for num in range(-30, 1)]
kyouhanten_code_list = kyouhanten_df['共販店コード'].tolist()
kyoten_code_list = kyoten_df['拠点コード'].tolist()
okyakusama_code_list = okyakusama_df['お客様コード'].tolist()
shimukesaki_code_list = shimukesaki_df['仕向先コード'].tolist()
make_code_list = make_df['メーカーコード'].tolist()

orders = []

for kyouhanten_code in kyouhanten_code_list:
    for kyoten_code in kyoten_code_list:
        for date in date_list:
            orders.extend(make_orders(kyouhanten_code, kyoten_code, date, 10))

nouki_shitei_file = []

for kyouhanten_code in kyouhanten_code_list:
    for okyakusama_code in okyakusama_code_list:
        for date in date_list:
            nouki_shitei_file.extend(make_nouki_shitei_file(kyouhanten_code,
                                                            okyakusama_code, date, 10))

nouhin = []
for kyouhanten_code in kyouhanten_code_list:
    for shimukesaki_code in shimukesaki_code_list:
        for make_code in make_code_list:
            for date in date_list:
                nouhin.extend(make_nouhin(kyouhanten_code,
                              shimukesaki_code, make_code, date, 10))


print(pd.DataFrame(orders))
print(pd.DataFrame(nouki_shitei_file))
print(pd.DataFrame(nouhin))
