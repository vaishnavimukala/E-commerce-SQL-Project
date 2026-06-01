import os
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="E-Commerce Analytics API")

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.get("/")
def home():
    return {"message": "E-Commerce Analytics API is running"}

@app.get("/revenue/total")
def total_revenue():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(total_amount)
        FROM orders
        WHERE order_status = 'Completed';
    """)

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {"total_revenue": float(result or 0)}

@app.get("/revenue/daily")
def daily_revenue():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            DATE(order_date) AS order_day,
            SUM(total_amount) AS daily_revenue
        FROM orders
        WHERE order_status = 'Completed'
        GROUP BY DATE(order_date)
        ORDER BY order_day;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"order_day": str(row[0]), "daily_revenue": float(row[1])}
        for row in rows
    ]

@app.get("/products/top")
def top_products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.product_name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.quantity * oi.item_price) AS total_sales
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'Completed'
        GROUP BY p.product_name, p.category
        ORDER BY total_sales DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "product_name": row[0],
            "category": row[1],
            "units_sold": int(row[2]),
            "total_sales": float(row[3])
        }
        for row in rows
    ]

@app.get("/customers/repeat")
def repeat_customers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.customer_id,
            c.name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS customer_lifetime_value
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.order_status = 'Completed'
        GROUP BY c.customer_id, c.name
        HAVING COUNT(o.order_id) > 1
        ORDER BY customer_lifetime_value DESC
        LIMIT 20;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "customer_id": row[0],
            "name": row[1],
            "total_orders": int(row[2]),
            "customer_lifetime_value": float(row[3])
        }
        for row in rows
    ]

@app.get("/inventory/low-stock")
def low_stock():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.product_name,
            p.category,
            i.stock_quantity,
            i.reorder_level
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.stock_quantity <= i.reorder_level
        ORDER BY i.stock_quantity ASC;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "product_name": row[0],
            "category": row[1],
            "stock_quantity": row[2],
            "reorder_level": row[3]
        }
        for row in rows
    ]