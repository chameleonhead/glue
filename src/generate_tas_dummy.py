import pandas as pd
import numpy as np
from faker import Factory
import os.path
import datetime

# create some fake data
fake = Factory.create('ja_JP')


def make_kyouhanten(num):
    return [{'共販店コード': x+1000, '共販店名': fake.company()} for x in range(num)]


def make_juchu_kyoten(num):
    return [{'受注拠点コード': x+1000, '受注拠点名': fake.administrative_unit() + fake.city()} for x in range(num)]


def make_hinban(num):
    return [{'品番': x+1000, '品名': fake.color_name()} for x in range(num)]


def load_or_create_csv(fname, factory, num):
    if os.path.isfile(fname):
        return pd.read_csv(fname)
    else:
        df = pd.DataFrame(factory(num=num))
        df.to_csv(fname, index=False)
        return df


kyouhanten_df = load_or_create_csv(
    'data/tas/kyouhanten.csv', make_kyouhanten, 100)
juchu_kyoten_df = load_or_create_csv(
    'data/tas/juchu_kyoten.csv', make_juchu_kyoten, 100)
hinban_df = load_or_create_csv('data/tas/hinban.csv', make_hinban, 100)


def make_orders(date, num):

    # lists to randomly assign to workers
    kyouhanten_code_list = kyouhanten_df['共販店コード'].tolist()
    juchu_kyoten_code_list = juchu_kyoten_df['受注拠点コード'].tolist()
    hinban_list = hinban_df['品番'].tolist()

    fake_orders = [{'共販店コード': np.random.choice(kyouhanten_code_list),
                    '受注拠点コード': np.random.choice(juchu_kyoten_code_list),
                    '受注日': date,
                    'アイテムNo.': item_no,
                    '品番': np.random.choice(hinban_list)} for item_no in range(1, 1 + num)]

    return fake_orders


def make_nouki_shitei_file(date, num):

    # lists to randomly assign to workers
    kyouhanten_code_list = kyouhanten_df['共販店コード'].tolist()
    juchu_kyoten_code_list = juchu_kyoten_df['受注拠点コード'].tolist()
    hinban_list = hinban_df['品番'].tolist()

    fake_orders = [{'共販店コード': np.random.choice(kyouhanten_code_list),
                    '受注拠点コード': np.random.choice(juchu_kyoten_code_list),
                    '受注日': date,
                    'アイテムNo.': item_no,
                    '品番': np.random.choice(hinban_list)} for item_no in range(1, 1 + num)]

    return fake_orders


print(kyouhanten_df.head())
print(juchu_kyoten_df.head())
print(hinban_df.head())

today = datetime.date.today()
date_list = [today + datetime.timedelta(days=num) for num in range(-30, 1)]
orders = []
for date in date_list:
    orders.extend(make_orders(date, 10))
print(pd.DataFrame(orders))
