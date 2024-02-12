import random
import names
import psycopg2
from faker import Faker
from math import floor


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


def getProductPrice(idProduct):
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


def insert_data_facts():
    idProduct = get_random_product_id()
    price = getProductPrice(idProduct)
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


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost"
    )
    cur = conn.cursor()
    fake = Faker()

    insert_shop(100)
    insert_product(100)
    insert_customer(100)

    cur.close()
    conn.close()
