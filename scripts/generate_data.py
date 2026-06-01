import os
import random
from faker import Faker
import psycopg2
from dotenv import load_dotenv

load_dotenv()
fake = Faker()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

categories = ["Electronics", "Fashion", "Books", "Sports", "Beauty", "Home"]

print("Inserting customers...")

for _ in range(1000):
    cur.execute("""
        INSERT INTO customers (name, email, city)
        VALUES (%s, %s, %s)
    """, (
        fake.name(),
        fake.unique.email(),
        fake.city()
    ))

conn.commit()

print("Inserting products...")

for _ in range(200):
    cur.execute("""
        INSERT INTO products (product_name, category, price)
        VALUES (%s, %s, %s)
    """, (
        fake.word().capitalize(),
        random.choice(categories),
        round(random.uniform(10, 1000), 2)
    ))

conn.commit()

print("Inserting inventory...")

for product_id in range(1, 201):
    cur.execute("""
        INSERT INTO inventory (product_id, stock_quantity, reorder_level)
        VALUES (%s, %s, %s)
    """, (
        product_id,
        random.randint(10, 500),
        random.randint(5, 50)
    ))

conn.commit()

print("Inserting orders and order items...")

for _ in range(5000):
    customer_id = random.randint(1, 1000)
    order_status = random.choice(["Completed", "Pending", "Cancelled"])

    cur.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount, order_status)
        VALUES (%s, %s, %s, %s)
        RETURNING order_id
    """, (
        customer_id,
        fake.date_time_between(start_date="-1y", end_date="now"),
        0,
        order_status
    ))

    order_id = cur.fetchone()[0]
    total_amount = 0

    for _ in range(random.randint(1, 5)):
        product_id = random.randint(1, 200)

        cur.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
        price = cur.fetchone()[0]

        quantity = random.randint(1, 4)
        total_amount += float(price) * quantity

        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, item_price)
            VALUES (%s, %s, %s, %s)
        """, (
            order_id,
            product_id,
            quantity,
            price
        ))

    cur.execute("""
        UPDATE orders
        SET total_amount = %s
        WHERE order_id = %s
    """, (
        round(total_amount, 2),
        order_id
    ))

conn.commit()

print("Inserting cart events...")

for _ in range(3000):
    cur.execute("""
        INSERT INTO cart_events (customer_id, product_id, event_type, event_time)
        VALUES (%s, %s, %s, %s)
    """, (
        random.randint(1, 1000),
        random.randint(1, 200),
        random.choice(["ADD_TO_CART", "REMOVE_FROM_CART", "CHECKOUT"]),
        fake.date_time_between(start_date="-6m", end_date="now")
    ))

conn.commit()

cur.close()
conn.close()

print("All fake e-commerce data inserted successfully!")