-- 1. Total revenue
SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE order_status = 'Completed';

-- 2. Daily revenue trend
SELECT 
    DATE(order_date) AS order_day,
    SUM(total_amount) AS daily_revenue
FROM orders
WHERE order_status = 'Completed'
GROUP BY DATE(order_date)
ORDER BY order_day;

-- 3. Top 10 products by sales
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

-- 4. Repeat customers
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
ORDER BY customer_lifetime_value DESC;

-- 5. Low stock products
SELECT 
    p.product_name,
    p.category,
    i.stock_quantity,
    i.reorder_level
FROM inventory i
JOIN products p ON i.product_id = p.product_id
WHERE i.stock_quantity <= i.reorder_level
ORDER BY i.stock_quantity ASC;

-- 6. Cart event summary
SELECT 
    event_type,
    COUNT(*) AS total_events
FROM cart_events
GROUP BY event_type
ORDER BY total_events DESC;