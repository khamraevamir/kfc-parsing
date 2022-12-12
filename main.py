import sqlite3 as sq
import os
import json
from database.db import Database

# Create

# ------------------------------------------------------------
# Category
category_table = Database(filename='database/kfc.db', table='category')

category_table.create('''
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        ''')

# ------------------------------------------------------------
# Product
product_table = Database(filename='database/kfc.db', table='product')
product_table.create('''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            image TEXT,
            category_id REFERENCES category(category_id)
        ''')

# ------------------------------------------------------------

# POST
# ------------------------------------------------------------

counter = 1
with open(f"json/categories.json", encoding='utf-8') as file:
    data = json.load(file)
    for item in data.keys():
        category_table.post(title=item)

        with open(f"json/{item}/{item}.json", encoding='utf-8') as product_file:
            category = json.load(product_file)

        for products in category:
            title = products['title']
            description = products['description']
            price = products['price']
            image = products['image']
            category_id = counter

            product_table.post(
                title=title,
                description=description,
                price=price,
                image=image,
                category_id=category_id
            )

        counter += 1

category_table.close()
product_table.close()

# ------------------------------------------------------------

# PUT
# ------------------------------------------------------------
# data_id = db.get(id='1')[0]
# data = {'title': 'Note 1!', 'checked': '1'}
# db.put(id=data_id, data=data)


# ------------------------------------------------------------

# GET
# ------------------------------------------------------------
# all_data = db.get_all()
# print(all_data)

# ------------------------------------------------------------

# DELETE
# ------------------------------------------------------------
# data_id = db.get(id='1')[0]
# db.delete(id=data_id)
