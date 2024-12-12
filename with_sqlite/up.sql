CREATE TABLE "restaurant" (
    restaurant_id INTEGER PRIMARY KEY, -- alias for SQlite's auto incremented ROWID
    name TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE "dish" (
    dish_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurant(restaurant_id) NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE "client" (
    client_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurant(restaurant_id) NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    inscription_date TEXT CHECK(inscription_date IS date(inscription_date)) NOT NULL
);

CREATE TABLE "order" (
    order_id INTEGER PRIMARY KEY,
    client_id INTEGER REFERENCES client(client_id) NOT NULL,
    order_date TEXT CHECK(order_date IS date(order_date)) NOT NULL,
    total_amount REAL NOT NULL
);

CREATE TABLE "employee" (
    employee_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurant(restaurant_id) NOT NULL,
    position TEXT CHECK(position IN ('HEAD COOK','COOK','DISHWASHER','MANAGER','WAITER')) NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    hiring_date TEXT CHECK(hiring_date IS date(hiring_date)) NOT NULL,
    salary REAL NOT NULL
);

CREATE TABLE "delivery" (
    delivery_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurant(restaurant_id) NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    delivery_date TEXT CHECK(delivery_date IS date(delivery_date)) NOT NULL
);

CREATE TABLE "supplier" (
    supplier_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL
);
