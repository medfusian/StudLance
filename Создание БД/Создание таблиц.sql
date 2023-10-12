-- Создание таблицы "User"
CREATE TABLE "User" (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  login VARCHAR(255)
);

-- Создание таблицы "Cart"
CREATE TABLE "Cart" (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2),
  count INT,
  summary NUMERIC,
  article INT,
  user_id INT,
  order_id INT,
  FOREIGN KEY (article) REFERENCES "Product"(article),
  FOREIGN KEY (user_id) REFERENCES "User"(id),
  FOREIGN KEY (order_id) REFERENCES "Order"(id)
);

-- Создание таблицы "Order"
CREATE TABLE "Order" (
  id SERIAL PRIMARY KEY,
  order_date TIMESTAMP,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES "User"(id)
);

-- Создание таблицы "Category"
CREATE TABLE "Category" (
  id SERIAL PRIMARY KEY,
  category VARCHAR(50),
  description TEXT,
  image BYTEA
);

CREATE TABLE "Color" (
    id SERIAL PRIMARY KEY,
    color VARCHAR(50)
)

-- Создание таблицы "Product"
CREATE TABLE "Product" (
  article INT PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  season VARCHAR(20),
  price NUMERIC(10, 2),
  image BYTEA,
  category INT,
  supplier INT,
  FOREIGN KEY (color) REFERENCES "Color"(id),
  FOREIGN KEY (category) REFERENCES "Category"(id),
  FOREIGN KEY (supplier) REFERENCES "Supplier"(id)
);

-- Создание таблицы "Supplier"
CREATE TABLE "Supplier" (
  id SERIAL PRIMARY KEY,
  supplier VARCHAR(50),
  country_id INT,
  FOREIGN KEY (country_id) REFERENCES "Country"(id)
);

-- Создание таблицы "Country"
CREATE TABLE "Country" (
  id SERIAL PRIMARY KEY,
  country VARCHAR(20)
);