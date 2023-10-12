SELECT *
FROM "Product"
WHERE color = 'Yellow';

SELECT order_date
FROM "Order"
WHERE "Order".user_id = 157;


SELECT u.id, u.email,
  (SELECT COUNT(*) FROM "Cart" c WHERE c.user_id = u.id) AS cart_count
FROM "User" u
ORDER BY cart_count DESC;

SELECT p.article, p.name,
  (SELECT SUM(c.price * c.count) FROM "Cart" c WHERE c.article = p.article) AS total_price
FROM "Product" p;


SELECT u.id, u.email, c.cart_count
FROM "User" u
JOIN (
  SELECT user_id, COUNT(*) AS cart_count
  FROM "Cart"
  GROUP BY user_id
) c ON u.id = c.user_id;

SELECT p.article, p.name, c.total_price
FROM "Product" p
JOIN (
  SELECT article, SUM(price * count) AS total_price
  FROM "Cart"
  GROUP BY article
) c ON p.article = c.article;


SELECT c.category, COUNT(p.article) AS product_count
FROM "Category" c
JOIN "Product" p ON c.id = p.category
GROUP BY c.category
ORDER BY product_count DESC;

SELECT u.id, u.email, SUM(p.price * c.count) AS total_purchase
FROM "User" u
JOIN "Cart" c ON u.id = c.user_id
JOIN "Product" p ON c.article = p.article
GROUP BY u.id, u.email
ORDER BY total_purchase;


SELECT *
FROM "User" u
WHERE EXISTS (
  SELECT 1
  FROM "Cart" c
  JOIN "Product" p ON c.article = p.article
  WHERE c.user_id = u.id
    AND p.price > (
      SELECT AVG(price)
      FROM "Product"
      WHERE category = p.category
    )
);

SELECT *
FROM "Product" p
WHERE EXISTS (
  SELECT 1
  FROM "Supplier" s
  JOIN "Country" c ON s.country_id = c.id
  WHERE p.supplier = s.id
    AND c.country = 'Iran'
);


SELECT
  id,
  order_date,
  LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date) AS previous_order_date
FROM "Order"
ORDER BY user_id, order_date;


SELECT c.category, COUNT(p.article) AS total_count
FROM "Category" c
JOIN "Product" p ON c.id = p.category
GROUP BY c.category;

SELECT s.id, s.supplier, AVG(p.price) AS average_price
FROM "Supplier" s
JOIN "Product" p ON s.id = p.supplier
GROUP BY s.id, s.supplier;

SELECT u.id, u.email, SUM(p.price * c.count) AS total_cost
FROM "User" u
JOIN "Cart" c ON u.id = c.user_id
JOIN "Product" p ON c.article = p.article
GROUP BY u.id, u.email;


SELECT article, name, color
FROM "Product" p
WHERE EXISTS (
  SELECT 1
  FROM "Cart" c
  WHERE c.article = p.article
);


SELECT id
FROM "User"
EXCEPT
SELECT user_id
FROM "Order";


SELECT u.id, u.email, c.id AS cart_id
FROM "User" u
LEFT JOIN "Cart" c ON u.id = c.user_id
WHERE c.id IS NOT NULL;


SELECT u.id, u.email, COUNT(p.article) AS total_products
FROM "User" u
JOIN "Cart" c ON u.id = c.user_id
JOIN "Product" p ON c.article = p.article
GROUP BY u.id, u.email;


SELECT
  CASE
    WHEN count < 5 THEN 'Мало товаров'
    WHEN count >= 5 AND count < 10 THEN 'Среднее количество товаров'
    ELSE 'Много товаров'
  END AS cart_quantity,
  SUM(price) AS total_price
FROM "Cart"
GROUP BY cart_quantity;


SELECT user_id, COUNT(article) AS total_products
FROM "Cart"
GROUP BY user_id
HAVING COUNT(article) > 2;


SELECT *
INTO backup_orders
FROM "Order"
WHERE order_date >= '2023-01-01';
