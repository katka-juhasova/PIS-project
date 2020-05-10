
SQLITE_INSERT_PRODUCT = '''
    INSERT INTO CIS_product(name, price, weight, breakable, image) VALUES (?, ?, ?, ?, ?)
'''

SQLITE_INSERT_PRODUCT_TO_STORE = '''
    INSERT INTO CIS_productsinstore(amount, product_id, store_id) VALUES (?, ?, ?)
'''

SQLITE_INSERT_COURIER = '''
    INSERT INTO CIS_courier(name, automobile, bicycle) VALUES (?, ?, ?)
'''

SQLITE_SELECT_ALL_STORES = '''
    SELECT * FROM CIS_store
'''

SQLITE_SELECT_MUNICIPALITY = '''
    SELECT municipality FROM CIS_address INNER JOIN CIS_store on CIS_store.address_id = CIS_address.id WHERE CIS_store.id = ?
'''

SQLITE_SELECT_CITY = '''
    SELECT city FROM CIS_address INNER JOIN CIS_store on CIS_store.address_id = CIS_address.id WHERE CIS_store.id = ?
'''

SQLITE_SELECT_PRODUCTS_IN_STORE = '''
    SELECT product_id FROM CIS_productsinstore WHERE store_id = ?
'''

SQLITE_SELECT_COURIER_ID = '''
    SELECT id FROM CIS_courier
'''

SQLITE_SELECT_COURIER_AUTOMOBILE = '''
    SELECT automobile FROM CIS_courier where id = ?
'''

SQLITE_SELECT_COURIER_BICYCLE = '''
    SELECT bicycle FROM CIS_courier where id = ?
'''

SQLITE_MISSING = '''
    SELECT amount FROM CIS_productsinstore WHERE store_id = ? AND product_id = ?
'''

SQLITE_ALTERNATIVE = '''
    SELECT alternative FROM CIS_alternative where product = ?
'''