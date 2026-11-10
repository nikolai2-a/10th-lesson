import json
from sqlalchemy import create_engine, ForeignKey, select, insert
from sqlalchemy import MetaData, Table, Column, Integer, String, Float


with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Загружено товаров: {len(catalog)}")

categories = {}
products = []

for item in catalog:
    cat = item["category"]
    cat_name = cat["name"]
    cat_desc = cat["description"]

    categories.setdefault(cat_name, cat_desc)

    products.append({
        "product_name": item["product_name"],
        "price": item["price"],
        "category_name": cat_name
    })

print(f"Уникальных категорий: {len(categories)}")
print(f"Товаров: {len(products)}")

engine = create_engine('sqlite:///catalog.db;')
engine.connect()
metadata = MetaData()

categories_table = Table(
    'categories',
    metadata,
    Column('id', Integer, primary_key = True),
    Column('name', String(100), nullable = False), 
    Column('description', String(100)),
    )

products_table = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key = True),
    Column('price', Float, nullable = False),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete ='CASCADE'), nullable = False),
    Column('product_name', String(100), nullable = False),
    )

metadata.create_all(engine)

with engine.connect() as connection:
    connection.execute(categories_table.delete())
    connection.execute(products_table.delete())
    
    for cat_name, cat_desc in categories.items():
        something = insert(categories_table).values(
            name = cat_name,
            description = cat_desc,
            )
        result = connection.execute(something)
        connection.commit()

with engine.connect() as connection:
    statement = select(categories_table.c.id, categories_table.c.name)
    result = connection.execute(statement)
    category_ids = {name: cat_id for cat_id, name in result}

products_data = [
    {
        "product_name": p["product_name"],
        "price": p["price"],
        "category_id": category_ids[p["category_name"]]
    }
    for p in products
]

with engine.connect() as connection:
    something = insert(products_table)
    result = connection.execute(something, products_data)
    connection.commit()





