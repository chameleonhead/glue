import pandas as pd
import numpy as np
from faker import Factory
import os
import datetime
import random

# create some fake data
fake = Factory.create('ja_JP')


def make_kyouhanten(kyouhanten_code):
    return {'共販店コード': kyouhanten_code, '共販店名': fake.company()}


def make_kyoten(kyoten_code):
    return {'拠点コード': kyoten_code, '拠点名': fake.administrative_unit() + fake.city()}


def make_hinban(hinban):
    return {'品番': hinban, '品名': fake.color_name()}


def make_okyakusama(okyakusama_code):
    return {'お客様コード': okyakusama_code, 'お客様名': fake.company()}


def make_shimukesaki(shimukesaki_code):
    return {'仕向先コード': shimukesaki_code, '仕向先名': fake.company()}


def make_make(make_code):
    return {'メーカーコード': make_code, 'メーカー名': fake.company()}


def load_or_create_csv(fname, factory, num):
    os.makedirs('data/tas', exist_ok=True)
    if os.path.isfile('data/tas/' + fname):
        return pd.read_csv('data/tas/' + fname)
    else:
        df = pd.DataFrame([factory(num=num) for num in range(num)])
        df.to_csv('data/tas/' + fname, index=False)
        return df


kyouhanten_df = load_or_create_csv(
    'kyouhanten.csv',
    lambda num: make_kyouhanten(num + 1000),
    10)
kyoten_df = load_or_create_csv(
    'kyoten.csv',
    lambda num: make_kyoten(num + 1000),
    10)
hinban_df = load_or_create_csv(
    'hinban.csv',
    lambda num: make_hinban(num + 1000),
    100)
okyakusama_df = load_or_create_csv(
    'okyakusama.csv',
    lambda num: make_okyakusama(num + 1000),
    100)
shimukesaki_df = load_or_create_csv(
    'shimukesaki.csv',
    lambda num: make_shimukesaki(num + 1000),
    100)
make_df = load_or_create_csv(
    'make.csv',
    lambda num: make_make(num + 1000),
    100)


def make_order(kyouhanten_code, juchu_kyoten_code, date, item_no, hinban):
    return {'共販店コード': kyouhanten_code,
            '受注拠点コード': juchu_kyoten_code,
            '受注日': date,
            'アイテムNo.': item_no,
            '品番': hinban}


def make_nouki_shitei_file(kyouhanten_code, hinban, juchu_kyoten_code, order_no, order_date):
    return {'共販店コード': kyouhanten_code,
            'お客様コード': np.random.choice(okyakusama_df['お客様コード']),
            '品番': hinban,
            'メーカー区分': np.random.choice(['自社生産', '仕入れ']),
            '入庫拠点': np.random.choice([juchu_kyoten_code, np.random.choice(kyoten_df['拠点コード'])]),
            '注文No.': order_no,
            '納期指定日': fake.date_between(start_date=order_date, end_date='+10d')}


def make_nouhin(kyouhanten_code, order_no, hinban, order_date):
    return {'共販店コード': kyouhanten_code,
            '仕向先コード': np.random.choice(shimukesaki_df['仕向先コード']),
            'メーカーコード': np.random.choice(make_df['メーカーコード']),
            'イシュNo.': order_no,
            'イシュ内連番': 1,
            '品番': hinban,
            'メーカー出荷日': fake.date_between(start_date=order_date, end_date='+10d'),
            '入庫入力日': fake.date_between(start_date=order_date, end_date='+10d')}


today = datetime.date.today()
date_list = [today + datetime.timedelta(days=num) for num in range(-30, 1)]
kyouhanten_code_list = kyouhanten_df['共販店コード'].tolist()
kyoten_code_list = kyoten_df['拠点コード'].tolist()


for date in date_list:
    for kyouhanten_code in kyouhanten_code_list:
        orders = []
        nouki_shitei_file = []
        nouhin = []

        for kyoten_code in kyoten_code_list:
            for num in range(10):
                hinban = np.random.choice(hinban_df['品番'])
                order = make_order(
                    kyouhanten_code,
                    kyoten_code,
                    date,
                    num,
                    hinban)
                orders.append(order)

                if (random.randint(0, 1) == 1):
                    nouki_shitei_file.append(
                        make_nouki_shitei_file(
                            kyouhanten_code,
                            hinban,
                            kyoten_code,
                            num,
                            date))

                nouhin.append(make_nouhin(
                    kyouhanten_code,
                    num,
                    hinban,
                    date))

        os.makedirs(
            f'data/tas/orders/{date.isoformat()}',
            exist_ok=True)
        pd.DataFrame(orders).to_csv(
            f'data/tas/orders/{date.isoformat()}/{kyouhanten_code}.csv',
            index=False)
        os.makedirs(
            f'data/tas/nouki_shitei_file/{date.isoformat()}',
            exist_ok=True)
        pd.DataFrame(nouki_shitei_file).to_csv(
            f'data/tas/nouki_shitei_file/{date.isoformat()}/{kyouhanten_code}.csv',
            index=False)
        os.makedirs(
            f'data/tas/nouhin/{date.isoformat()}',
            exist_ok=True)
        pd.DataFrame(nouhin).to_csv(
            f'data/tas/nouhin/{date.isoformat()}/{kyouhanten_code}.csv',
            index=False)
