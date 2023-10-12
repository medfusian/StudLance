from faker import Faker
import psycopg2
import random

fake = Faker()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="fabrics",
    user="postgres",
    password="open38ai12"
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Генерация и вставка 1000 значений в таблицу "User"
for _ in range(1000):
    email = fake.email()
    password = fake.password()
    login = fake.user_name()

    cur.execute("""
        INSERT INTO "User" (email, password, login)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING
    """, (email, password, login))

# Генерация и вставка 50 значений в таблицу "Order"
for _ in range(50):
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    user_id = random.randint(1, 1000)

    cur.execute("""
        INSERT INTO "Order" (order_date, user_id)
        VALUES (%s, %s)
    """, (order_date, user_id))

# Генерация и вставка 50 значений в таблицу "Country"
for _ in range(50):
    country = fake.country()

    cur.execute("""
        INSERT INTO "Country" (country)
        VALUES (%s)
    """, (country,))

# Генерация и вставка 50 значений в таблицу "Supplier"
for _ in range(50):
    supplier = fake.company()
    country_id = random.randint(1, 50)

    cur.execute("""
        INSERT INTO "Supplier" (supplier, country_id)
        VALUES (%s, %s)
    """, (supplier, country_id))

# Генерация и вставка 50 значений в таблицу "Category"
for _ in range(50):
    category = fake.word()
    description = fake.text()
    image = bytes([random.randint(0, 255) for _ in range(10)])

    cur.execute("""
        INSERT INTO "Category" (category, description, image)
        VALUES (%s, %s, %s)
    """, (category, description, image))

# Генерация и вставка 50 значений в таблицу "Product"
for article in range(1, 51):
    name = fake.word()
    description = fake.text()
    season = fake.word()
    color = fake.color_name()
    price = round(random.uniform(10.0, 100.0), 2)
    image = bytes([random.randint(0, 255) for _ in range(10)])
    category = random.randint(1, 50)
    supplier = random.randint(1, 50)

    cur.execute("""
        INSERT INTO "Product" (article, name, description, season, color, price, image, category, supplier)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (article, name, description, season, color, price, image, category, supplier))

# Генерация и вставка 50 значений в таблицу "Cart"
for _ in range(50):
    price = round(random.uniform(1.0, 100.0), 2)
    count = random.randint(1, 10)
    summary = price * count
    article = random.randint(1, 50)
    user_id = random.randint(1, 1000)
    order_id = random.randint(1, 50)

    cur.execute("""
        INSERT INTO "Cart" (price, count, summary, article, user_id, order_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (price, count, summary, article, user_id, order_id))

# Сохранение изменений в базе данных
conn.commit()

# Закрытие соединения
cur.close()
conn.close()
