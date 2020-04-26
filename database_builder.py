import sqlite3
import random
from CIS.sql_queries import SQLITE_INSERT_PRODUCT
from CIS.sql_queries import SQLITE_INSERT_PRODUCT_TO_STORE
from CIS.sql_queries import SQLITE_INSERT_COURIER


vegetables = {
    'ananás': 'images/item0.png',
    'avokádo': 'images/item1.png',
    'baklažán': 'images/item2.png',
    'banány': 'images/item3.png',
    'brokolica': 'images/item4.png',
    'broskyňa': 'images/item5.png',
    'cesnak': 'images/item6.png',
    'cibuľa': 'images/item7.png',
    'citróny': 'images/item8.png',
    'cukina': 'images/item9.png',
    'čerešne': 'images/item10.png',
    'červená repa': 'images/item11.png',
    'čučoriedky': 'images/item12.png',
    'figy': 'images/item13.png',
    'grapefruit': 'images/item14.png',
    'hlávkový šalát': 'images/item15.png',
    'hliva ustricová': 'images/item16.png',
    'hrášok': 'images/item17.png',
    'hrozno': 'images/item18.png',
    'hruška': 'images/item19.png',
    'chren': 'images/item20.png',
    'jablko': 'images/item21.png',
    'jahody': 'images/item22.png',
    'kaki': 'images/item23.png',
    'kaleráb': 'images/item24.png',
    'karfiol': 'images/item25.png',
    'kivi': 'images/item26.png',
    'ľadový šalát': 'images/item27.png',
    'liči': 'images/item28.png',
    'maliny': 'images/item29.png',
    'mandarínky': 'images/item30.png',
    'mango': 'images/item31.png',
    'marhule': 'images/item32.png',
    'melón': 'images/item33.png',
    'mrkva': 'images/item34.png',
    'nektárinka': 'images/item35.png',
    'paprika': 'images/item36.png',
    'paradajky': 'images/item37.png',
    'pažítka': 'images/item38.png',
    'pekinská kapusta': 'images/item39.png',
    'petržlen': 'images/item40.png',
    'poľníček': 'images/item41.png',
    'pomaranč': 'images/item42.png',
    'pomelo': 'images/item43.png',
    'rebarbora': 'images/item44.png',
    'reďkovka': 'images/item45.png',
    'ríbezle': 'images/item46.png',
    'rukola': 'images/item47.png',
    'slivky': 'images/item48.png',
    'struková fazuľka': 'images/item49.png',
    'šampiňóny': 'images/item50.png',
    'špargľa': 'images/item51.png',
    'špenát': 'images/item52.png',
    'tekvica': 'images/item53.png',
    'uhorka': 'images/item54.png',
    'zázvor': 'images/item55.png',
    'zeler vňaťový': 'images/item56.png',
    'zemiaky': 'images/item57.png'
}

'''
WARNING!!! Always put your new piece of code into main comment the previous 
parts, we don't wanna have multiple rows with "ananas" in the db table
'''

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # for vegetable in vegetables:
    #     image = vegetables[vegetable]
    #     price = round(random.uniform(0.50, 5.00), 1)
    #     weight = round(random.uniform(0.50, 5.00), 1)
    #     breakable = random.choice((True, False))
    #     data = (vegetable.capitalize(), price, weight, breakable, image)
    #     cursor.execute(SQLITE_INSERT_PRODUCT, data)
    #
    # conn.commit()

    # for store_id in [1, 2, 3, 4, 5, 7, 9, 10]:
    #     leave_out = list()
    #     for _ in range(10):
    #         leave_out.append(random.randint(1, 58))
    #
    #     for product_id in range(1, 59):
    #         if product_id not in leave_out:
    #             data = (50, product_id, store_id)
    #             cursor.execute(SQLITE_INSERT_PRODUCT_TO_STORE, data)
    #
    # conn.commit()

    couriers = ['Kurier Expres', 'Bolt Kuriér', 'GLS', 'GO4', 'Švihaj Kuriér',
                'DPD', 'Kurier Diamond', 'REX', 'Der Kurier', 'LUCKER s.r.o.']

    for i in range(10):
        bicycle = random.choice([True, False])
        automobile = random.choice([True, False]) if not bicycle else True
        data = (couriers[i], automobile, bicycle)
        cursor.execute(SQLITE_INSERT_COURIER, data)

    conn.commit()
