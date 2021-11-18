import pandas as pd
import numpy as np
from faker import Factory
import os.path
import datetime
import uuid

# create some fake data
fake = Factory.create('ja_JP')


def make_shimukesaki(num):
    return [{'仕向先コード': x+1000, '仕向先名': fake.company()} for x in range(num)]


def make_hinban(num):
    return [{'品番': x+1000, '品名': fake.color_name()} for x in range(num)]


def load_or_create_csv(fname, factory, num):
    if os.path.isfile(fname):
        return pd.read_csv(fname)
    else:
        df = pd.DataFrame(factory(num=num))
        df.to_csv(fname, index=False)
        return df


shimukesaki_df = load_or_create_csv(
    'data/tas/shimukesaki.csv', make_shimukesaki, 100)
hinban_df = load_or_create_csv('data/tas/hinban.csv', make_hinban, 100)


def make_orders(shimukesaki_code, order_number, date, num):

    hinban_list = hinban_df['品番'].tolist()

    fake_orders = [{'オーダーキー': uuid.uuid4(),
                    '仕向け先コード': shimukesaki_code,
                    'オーダーNO': order_number,
                    '受注日': date,
                    '品番': np.random.choice(hinban_list)} for _ in range(1, 1 + num)]

    return fake_orders


print(hinban_df.head())
print(shimukesaki_df.head())

today = datetime.date.today()
date_list = [today + datetime.timedelta(days=num) for num in range(-30, 1)]
shimukesaki_code_list = shimukesaki_df['仕向先コード'].tolist()

orders = []

for shimukesaki_code in shimukesaki_code_list:
    for date in date_list:
        orders.extend(make_orders(shimukesaki_code, 1000, date, 10))


print(pd.DataFrame(orders))
