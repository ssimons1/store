																
-- create database and use it
CREATE database store;
USE store;
DROP database if exists store;

-- create categories table with primary id key
CREATE TABLE categories(
id INT auto_increment,
name VARCHAR(30),
PRIMARY KEY (id)
);

-- create products table with primary id key and with foreign category key
CREATE TABLE products(
category INT,
description VARCHAR(200),
price DOUBLE,
title VARCHAR(100),
favorite BOOLEAN,
img_url VARCHAR(100),
id INT auto_increment,
PRIMARY KEY (id)
);

-- insert categories into category table
INSERT INTO categories (name) VALUES ('clothes'), ('cars'), ('food');

-- insert products into products table
INSERT INTO products (category, description, price, title, favorite, img_url) VALUES (1,'Black Dress',55.0,'ASOS Extreme Fringe Back Maxi Dress',1,'./images/black_dress.jpg'),(1, 'Red Shorts', 38.50,'ASOS PETITE Culotte Shorts',0,'./images/red_shorts.jpg'),(1,'Blue Top', 28.0,'ASOS Denim Top in Midwash Blue With Exaggerated Shoulder',0,'./images/blue_top.jpg'),(3,'Warm asian soup', 5.50,'Miso Soup',0,'./images/miso_soup.jpeg'),(2,'Red, beautiful, fast, expensive', 220000.0,'Ferrari',1,'./images/red_ferrari.jpg'),(2,'Older model regular black Ford',28950.0,'Ford',0,'./images/ford.jpeg'),(2,'Black with white stripe, sports', 37650.0,'Mini Cooper',1,'./images/mini_cooper.jpg'),(3,'Medium cooked meat', 52.0,'Steak',1,'./images/steak.jpg'),(3,'Warm boiled peas', 4.35,'Peas',1,'./images/peas.jpg'),(3,'Hot liquid chocolate in center', 15.75,'Chocolate Souffle',1,'./images/chocolate_souffle.jpg');

SELECT categories.name, products.* FROM products LEFT JOIN categories ON categories.id=products.category group by categories.name order by categories.name, products.title asc;
