import datetime
import random
from math import floor

import names
import psycopg2
from faker import Faker


def generate_random_phone_number():
    first_digit = random.choice(["6", "7"])
    remaining_digits = [str(random.randint(0, 9)) for _ in range(9)]
    phone_number = "0{}-{}{}-{}{}-{}{}-{}{}".format(
        first_digit, *remaining_digits[:2], *remaining_digits[2:4], *remaining_digits[4:6], *remaining_digits[6:8],
        *remaining_digits[8:]
    )
    return phone_number


def get_random_product_id():
    cur.execute('SELECT id FROM product ORDER BY random() LIMIT 1')
    random_id = cur.fetchone()
    return random_id[0]


def get_random_shop_id():
    cur.execute("SELECT id FROM shop ORDER BY random() LIMIT 1")
    random_id = cur.fetchone()
    return random_id[0]


def get_random_customer_id():
    cur.execute('SELECT id FROM customer ORDER BY random() LIMIT 1')
    random_id = cur.fetchone()
    return random_id[0]


def get_random_time_id():
    cur.execute('SELECT id from time ORDER BY random() LIMIT 1')
    random_id = cur.fetchone()
    return random_id[0]


def get_product_price(idProduct):
    cur.execute('SELECT cents_price FROM product WHERE id = %s', (idProduct,))
    productPrice = cur.fetchone()
    return productPrice[0]


def insert_shop(nbRow):
    for i in range(nbRow):
        cur.execute("INSERT INTO shop (name, description, type)"
                    "VALUES (%s, %s, %s)",
                    (fake.word(), fake.text(max_nb_chars=100), fake.word()))
        conn.commit()


def insert_product(nbRow):
    for i in range(nbRow):
        cur.execute("INSERT INTO product (name, description, cents_price)"
                    "VALUES (%s, %s, %s)",
                    (fake.word(), fake.text(max_nb_chars=100), round(random.uniform(0.0, 100.0), 2)))
        conn.commit()


def insert_customer(nbRow):
    for i in range(nbRow):
        cur.execute("INSERT INTO customer (first_name, last_name, birth_date, phone_number) "
                    "VALUES (%s, %s, %s, %s)",
                    (names.get_first_name(), names.get_last_name(), fake.date(),
                     generate_random_phone_number()))
        conn.commit()


def insert_time(nbRow):
    for i in range(nbRow):
        random_datetime = fake.date_time_this_year()
        random_datetime_obj = datetime.datetime.strptime(random_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                                                         '%Y-%m-%d %H:%M:%S')
        date = random_datetime_obj.date()
        year, week, _ = random_datetime.isocalendar()
        month = random_datetime_obj.month

        cur.execute("INSERT INTO time (date,week,week_year,month,month_year,year)"
                    "VALUES (%s, %s, %s, %s,%s,%s)",
                    (
                        date,
                        week,
                        str(week) + "-" + str(year),
                        month,
                        str(month) + "-" + str(year),
                        year
                    ))
        conn.commit()


def insert_sale(nbRow):
    for i in range(nbRow):
        idProduct = get_random_product_id()
        price = get_product_price(idProduct)
        qty = random.randint(1, 10)
        total_price = round(qty * price, 2)
        cur.execute("INSERT INTO sale (id_customer,id_shop,id_product, quantity, total_cents_price,points_earned)"
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (get_random_customer_id(),
                     get_random_shop_id(),
                     idProduct,
                     qty,
                     total_price,
                     floor(total_price)))
        conn.commit()


def insert_customer_log(nbRow):
    for i in range(nbRow):
        duration_delta = datetime.timedelta(seconds=random.randint(1, 3600))
        id_customer = get_random_customer_id()
        id_time = get_random_time_id()

        seconds = duration_delta.total_seconds()
        interval_string = f"'{seconds} seconds'"

        cur.execute("INSERT INTO customer_log (id_customer, id_time, connection_time)"
                    "VALUES (%s, %s, INTERVAL %s)",
                    (id_customer, id_time, interval_string))
        conn.commit()


def insert_consultation(nbRow):
    for i in range(nbRow):
        id_time = get_random_time_id()
        id_product = get_random_product_id()
        consultations = random.randint(1, 500)
        cur.execute("INSERT INTO consultation (id_time, id_product, nb_consultations)"
                    "VALUES (%s, %s, %s)",
                    (id_time,
                     id_product,
                     consultations))
        conn.commit()


def insert_gift_purchase(nbRow):
    for i in range(nbRow):
        id_time = get_random_time_id()
        id_customer = get_random_customer_id()
        id_shop = get_random_shop_id()
        points_price = random.randint(1, 50)

        cur.execute("INSERT INTO gift_purchase (id_time, id_customer, id_shop,points_price)"
                    "VALUES (%s, %s, %s, %s)",
                    (id_time,
                     id_customer,
                     id_shop,
                     points_price))
        conn.commit()


def insert_retailer_registration(nbRow):
    for i in range(nbRow):
        id_time = get_random_time_id()
        id_shop = get_random_shop_id()
        cur.execute("INSERT INTO retailer_registration (id_time, id_shop)"
                    "VALUES (%s, %s)",
                    (id_time,
                     id_shop))
        conn.commit()


def insert_vfp_status(nbRow):
    for i in range(nbRow):
        id_customer = get_random_customer_id()
        id_time_start = get_random_time_id()
        id_time_end = get_random_time_id()
        perk_claimed = random.randint(1, 20)
        cur.execute("INSERT INTO vfp_status (id_customer, start_time, end_time, perk_claimed)"
                    "VALUES (%s, %s, %s, %s)",
                    (id_customer,
                     id_time_start,
                     id_time_end,
                     perk_claimed))
        conn.commit()


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost"
    )
    cur = conn.cursor()
    fake = Faker()

    # Insert in dimensions tables
    insert_shop(100)
    insert_product(100)
    insert_customer(100)
    insert_time(100)

    # Insert in facts table
    insert_sale(100)
    insert_customer_log(100)
    insert_consultation(100)
    insert_gift_purchase(100)
    insert_retailer_registration(100)
    insert_vfp_status(100)

    cur.close()
    conn.close()
