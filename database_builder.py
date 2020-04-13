import sqlite3
import random
from faker import Faker


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

sqlite_insert_product = """
    INSERT INTO CIS_product(name, price, weight, breakable, image) VALUES (?, ?, ?, ?, ?)
 """


if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    for vegetable in vegetables:
        image = vegetables[vegetable]
        price = round(random.uniform(0.50, 5.00), 1)
        weight = round(random.uniform(0.50, 5.00), 1)
        breakable = random.choice((True, False))
        data = (vegetable.capitalize(), price, weight, breakable, image)
        cursor.execute(sqlite_insert_product, data)

    conn.commit()
