import random

import names
import psycopg2
from faker import Faker

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost"
)

cur = conn.cursor()
fake = Faker()


def generate_random_phone_number():
    first_digit = random.choice(["6", "7"])
    remaining_digits = [str(random.randint(0, 9)) for _ in range(9)]
    phone_number = "0{}-{}{}-{}{}-{}{}-{}{}".format(
        first_digit, *remaining_digits[:2], *remaining_digits[2:4], *remaining_digits[4:6], *remaining_digits[6:8],
        *remaining_digits[8:]
    )
    return phone_number


def insert_data():
    # Insert data in customer
    cur.execute("INSERT INTO customer (first_name, last_name, birth_date, phone_number) "
                "VALUES (%s, %s, %s, %s)",
                (names.get_first_name(), names.get_last_name(), fake.date(),
                 generate_random_phone_number()))
    conn.commit()

    cur.execute("INSERT INTO product (name, description, cents_price)"
                "VALUES (%s, %s, %s)",
                (fake.word(), fake.text(max_nb_chars=100), round(random.uniform(0.0, 100.0), 2)))
    conn.commit()

    cur.execute("INSERT INTO shop (name, description, type)"
                "VALUES (%s, %s, %s)",
                (fake.word(), fake.text(max_nb_chars=100), fake.word()))
    conn.commit()

    week = fake.random_int(min=1, max=52)
    month = fake.random_int(min=1, max=12)
    year = fake.random_int(min=2000, max=2024)
    cur.execute("INSERT INTO time (date, week, week_year,month,month_year,year)"
                "VALUES (%s, %s, %s,%s, %s, %s)",
                (fake.date(),
                 week,
                 "{:02d}{:04d}".format(week, year),
                 month,
                 "{:02d}{:04d}".format(month, year),
                 year
                 ))

    conn.commit()


for i in range(100000):
    insert_data()

cur.close()
conn.close()
