-- VIEW 1: Monthly revenue
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp)::DATE AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.freight_value), 2) AS shipping_revenue,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_customer_spend
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1;


-- VIEW 2: Product category performance
CREATE OR REPLACE VIEW category_performance AS
SELECT
    COALESCE(p.product_category_name, 'unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(*) AS items_sold,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1;


-- VIEW 3: State-level sales performance
CREATE OR REPLACE VIEW state_performance AS
SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(
        SUM(oi.price) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state;