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

)