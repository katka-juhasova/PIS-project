
SQLITE_INSERT_PRODUCT = '''
    INSERT INTO CIS_product(name, price, weight, breakable, image) VALUES (?, ?, ?, ?, ?)
'''

SQLITE_INSERT_PRODUCT_TO_STORE = '''
    INSERT INTO CIS_productsinstore(amount, product_id, store_id) VALUES (?, ?, ?)
'''

SQLITE_INSERT_COURIER = '''
    INSERT INTO CIS_courier(name, automobile, bicycle) VALUES (?, ?, ?)
'''