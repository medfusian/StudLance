-- Создание триггера "calculate_summary"
CREATE OR REPLACE FUNCTION calculate_summary()
RETURNS TRIGGER AS $$
BEGIN
  NEW.summary := NEW.price * NEW.count; -- Вычисляем общую сумму товаров в корзине

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Привязка триггера к таблице "Cart"
CREATE TRIGGER calculate_summary_trigger
BEFORE INSERT OR UPDATE ON "Cart"
FOR EACH ROW
EXECUTE FUNCTION calculate_summary();


-- Функции
CREATE OR REPLACE FUNCTION get_total_order_price(order_id INT)
RETURNS NUMERIC AS $$
DECLARE
  total_price NUMERIC;
BEGIN
  SELECT SUM(price * count)
  INTO total_price
  FROM "Cart"
  WHERE "Cart".order_id = get_total_order_price.order_id;

  RETURN total_price;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_product_count_by_category(category_id INT)
RETURNS TABLE (category VARCHAR(50), product_count INT) AS $$
BEGIN
  RETURN QUERY
  SELECT c.category, COUNT(p.article) AS product_count
  FROM "Category" c
  LEFT JOIN "Product" p ON c.id = p.category
  WHERE c.id = get_product_count_by_category.category_id
  GROUP BY c.category;
END;
$$ LANGUAGE plpgsql;



-- Представления
CREATE OR REPLACE VIEW view_product_summary AS
SELECT p.article, p.name, p.price, c.category, s.supplier
FROM "Product" p
JOIN "Category" c ON p.category = c.id
JOIN "Supplier" s ON p.supplier = s.id;


CREATE OR REPLACE VIEW view_order_summary AS
SELECT o.id AS order_id, o.order_date, u.email, SUM(c.summary) AS total_price
FROM "Order" o
JOIN "User" u ON o.user_id = u.id
JOIN "Cart" c ON o.id = c.order_id
GROUP BY o.id, o.order_date, u.email;




-- Процедуры
CREATE OR REPLACE PROCEDURE insert_product(
  article INT,
  name VARCHAR(255),
  description TEXT,
  season VARCHAR(20),
  color VARCHAR(60),
  price NUMERIC(10, 2),
  image BYTEA,
  category_id INT,
  supplier_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO "Product" (article, name, description, season, color, price, image, category, supplier)
  VALUES (article, name, description, season, color, price, image, category_id, supplier_id);

  COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE update_product_price(
  article INT,
  new_price NUMERIC(10, 2)
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE "Product"
  SET price = new_price
  WHERE article = update_product_price.article;

  COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_product(article INT)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM "Product"
  WHERE "Product".article = delete_product.article;

  DELETE FROM "Cart"
  WHERE "Cart".article = delete_product.article;

  COMMIT;
END;
$$;


CREATE OR REPLACE PROCEDURE process_order(order_id INT)
LANGUAGE plpgsql
AS $$
BEGIN
  BEGIN TRANSACTION;

  UPDATE "Order"
  SET order_date = current_timestamp
  WHERE id = process_order.order_id;

  IF EXISTS (
    SELECT 1
    FROM "Cart"
    WHERE "Cart".order_id = process_order.order_id
  ) THEN
    DELETE FROM "Cart"
    WHERE "Cart".order_id = process_order.order_id;
  ELSE
    RAISE EXCEPTION 'No items in cart. Cannot process empty order.';
  END IF;

  COMMIT;
EXCEPTION
  WHEN others THEN
    ROLLBACK;
    RAISE;
END;
$$;


CREATE OR REPLACE PROCEDURE get_order_total_price(order_id INT, OUT total_price NUMERIC)
LANGUAGE plpgsql
AS $$
BEGIN
  SELECT SUM(c.summary)
  INTO total_price
  FROM "Cart" c
  WHERE c.order_id = get_order_total_price.order_id;

  IF total_price IS NULL THEN
    total_price := 0;
  END IF;
END;
$$;


