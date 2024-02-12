CREATE TABLE time(
    id SERIAL PRIMARY KEY,
    date DATE,
    week BIGINT,
    week_year varchar(6),
    month integer,
    month_year varchar(6),
    year integer
);

CREATE TABLE shop(
    id SERIAL PRIMARY KEY,
    name varchar(50),
    description varchar(255),
    type varchar(20)
);

CREATE TABLE product(
    id SERIAL PRIMARY KEY,
    name varchar(20),
    description varchar(255),
    cents_price float
);

CREATE TABLE customer(
    id SERIAL PRIMARY KEY,
    first_name varchar(20),
    last_name varchar(20),
    birth_date DATE,
    phone_number varchar(20)
);

CREATE TABLE sale(
    id SERIAL PRIMARY KEY,
    id_customer integer,
    id_shop integer,
    id_product integer,
    quantity integer,
    total_cents_price float,
    points_earned integer,
    FOREIGN KEY (id_customer) references customer(id),
    FOREIGN KEY (id_product) references product(id),
    FOREIGN KEY (id_shop) references shop(id)

);
CREATE TABLE customer_log(
    id serial PRIMARY KEY,
    id_customer integer,
    id_time integer,
    connection_time interval SECOND,
    FOREIGN KEY (id_customer) references customer(id),
    FOREIGN KEY (id_time) references time(id)
);

CREATE TABLE consultation(
    id SERIAL PRIMARY KEY,
    id_time integer,
    id_product integer,
    nb_consultations integer,
    FOREIGN KEY (id_time) references time(id),
    FOREIGN KEY (id_product) references product(id)
);
CREATE TABLE vfp_status(
    id SERIAL PRIMARY KEY,
    id_customer integer,
    start_time integer,
    end_time integer,
    perk_claimed integer,
    FOREIGN KEY (id_customer) references customer(id),
    FOREIGN KEY (start_time) references time(id),
    FOREIGN KEY (end_time) references  time(id)
);

    CREATE TABLE gift_purchase(
    id SERIAL PRIMARY KEY,
    id_time integer,
    id_customer integer,
    id_shop integer,
    points_price integer,
    FOREIGN KEY (id_time) references time(id),
    FOREIGN KEY (id_customer) references customer(id),
    FOREIGN KEY (id_shop) references shop(id)
);

CREATE TABLE retailer_registration(
    id SERIAL PRIMARY KEY,
    id_time integer,
    id_shop integer,
    FOREIGN KEY (id_time) references time(id),
    FOREIGN KEY (id_shop) references shop(id)
);
