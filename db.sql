CREATE DATABASE db_rental_mobil;
USE db_rental_mobil;

CREATE TABLE brands (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    brand_id INT,
    name VARCHAR(100),
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE TABLE cars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_id INT,
    plate_number VARCHAR(20),
    color VARCHAR(50),
    year INT,
    rental_price INT,
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    FOREIGN KEY (type_id) REFERENCES types(id)
);

CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nik VARCHAR(16),
    name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    car_id INT,
    pickup_date DATE,
    return_date DATE,
    guarantee_item VARCHAR(255),
    total_price INT,
    payment_method ENUM('cash', 'transfer'),
    status ENUM('rented', 'returned', 'cancelled') DEFAULT 'rented',
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (car_id) REFERENCES cars(id)
);

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    password VARCHAR(255),
    role ENUM('admin', 'petugas') DEFAULT 'admin'
);

INSERT INTO users (name, password, role) VALUES ('admin', 'admin123', 'admin');