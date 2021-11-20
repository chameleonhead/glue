import pandas as pd
import numpy as np
from faker import Factory
import os.path
import datetime
import uuid
import random

# create some fake data
fake = Factory.create('ja_JP')


def load_or_create_csv(fname, factory, num):
    pdir = os.path.dirname(fname)
    os.makedirs(pdir, exist_ok=True)
    if os.path.isfile(fname):
        return pd.read_csv(fname)
    else:
        df = pd.DataFrame([factory(num=num) for num in range(num)])
        df.to_csv(fname, index=False)
        return df


def write_to_csv(fname, df):
    pdir = os.path.dirname(fname)
    os.makedirs(pdir, exist_ok=True)
    df.to_csv(fname, index=False)


def make_shimukesaki(shimukesaki_code):
    return {'仕向先コード': shimukesaki_code, '仕向先名': fake.company()}


def make_hinban(hinban):
    return {'品番': hinban, '品名': fake.color_name()}


shimukesaki_df = load_or_create_csv(
    'data/atop/shimukesaki.csv',
    lambda num: make_shimukesaki(num + 1000),
    100)
hinban_df = load_or_create_csv(
    'data/atop/hinban.csv',
    lambda num: make_hinban(num + 1000),
    100)


def make_order(order_key, shimukesaki_code, order_number, order_date, hinban):
    return {'オーダーキー': order_key,
            '仕向け先コード': shimukesaki_code,
            'オーダーNO': order_number,
            '受注日': order_date,
            '品番': hinban}


def make_order_shiji_file(order_key, short_key, order_date, hinban, hinmei):
    return {'オーダーキー': order_key,
            '短縮キー': short_key,
            '受注リリース日': fake.date_between(start_date=order_date, end_date='+10d'),
            '出荷品番': hinban,
            '出荷品名': hinmei,
            '格納拠点区分': np.random.choice(['格納拠点区分1', '格納拠点区分2']),
            '出庫ロケ': '出庫ロケ',
            '納入予定日': fake.date_between(start_date=order_date, end_date='+10d'),
            'B/O引当リリース日': fake.date_between(start_date=order_date, end_date='+10d')}


def make_order_shiji_status_file(order_key, short_key, hinban):
    return {'オーダーキー': order_key,
            '短縮キー': short_key,
            '出荷品番': hinban}


def make_bo_nouki_kaito_file(order_key, short_key, order_date, hinban, order_number):
    return {'オーダーキー': order_key,
            '短縮キー': short_key,
            '受注リリース日': fake.date_between(start_date=order_date, end_date='+10d'),
            '出荷品番': hinban,
            'オーダーNO': order_number}


today = datetime.date.today()
date_list = [today + datetime.timedelta(days=num) for num in range(-30, 1)]
shimukesaki_code_list = shimukesaki_df['仕向先コード'].tolist()

orders = []
order_shiji_files = []
order_shiji_status_files = []
bo_nouki_kaito_files = []

for date in date_list:
    for shimukesaki_code in shimukesaki_code_list:
        for order_number in range(10):
            order_key = uuid.uuid4()
            hinban_data = hinban_df.sample()

            hinban = hinban_data['品番'].values[0]
            hinmei = hinban_data['品名'].values[0]
            order = make_order(order_key, shimukesaki_code,
                               order_number, date, hinban)
            orders.append(order)

            short_key = random.randint(0, 1000)
            order_shiji_file = make_order_shiji_file(
                order_key,
                short_key,
                date,
                hinban,
                hinmei)
            order_shiji_files.append(order_shiji_file)

            order_shiji_status_file = make_order_shiji_status_file(
                order_key,
                short_key,
                hinban)
            order_shiji_status_files.append(order_shiji_status_file)

            bo_nouki_kaito_file = make_bo_nouki_kaito_file(
                order_key,
                short_key,
                date,
                hinban,
                order_number)
            bo_nouki_kaito_files.append(bo_nouki_kaito_file)


write_to_csv(
    f'data/atop/orders.csv',
    pd.DataFrame(orders))
write_to_csv(
    f'data/atop/order_shiji_files.csv',
    pd.DataFrame(order_shiji_files))
write_to_csv(
    f'data/atop/order_shiji_status_files.csv',
    pd.DataFrame(order_shiji_status_files))
write_to_csv(
    f'data/atop/bo_nouki_kaito_files.csv',
    pd.DataFrame(bo_nouki_kaito_files))
