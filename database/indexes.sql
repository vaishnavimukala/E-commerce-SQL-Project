CREATE INDEX idx_orders_order_date 
ON orders(order_date);

CREATE INDEX idx_orders_customer_id 
ON orders(customer_id);

CREATE INDEX idx_orders_status 
ON orders(order_status);

CREATE INDEX idx_order_items_order_id 
ON order_items(order_id);

CREATE INDEX idx_order_items_product_id 
ON order_items(product_id);

CREATE INDEX idx_cart_events_customer_id 
ON cart_events(customer_id);

CREATE INDEX idx_cart_events_event_type 
ON cart_events(event_type);