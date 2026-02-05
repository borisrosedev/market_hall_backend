-- creation de table users 
CREATE TABLE ecommerce.users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    telephone VARCHAR(15),
    date_inscription DATE DEFAULT CURRENT_DATE,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- creation de table tages 
CREATE TABLE ecommerce.tags (
id SERIAL PRIMARY KEY ,
nom VARCHAR (50) UNIQUE NOT NULL,
description text,
date_creation DATE DEFAULT CURRENT_DATE
)
-- TALBE PRODUIT
CREATE TABLE ecommerce.products (
id SERIAL PRIMARY KEY,
nom VARCHAR (100) not null,
description text,
prix DECIMAL (10, 2),
stock INT DEFAULT 0,
date_creation DATE DEFAULT CURRENT_DATE,
date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- création talbe tags_proudit 
CREATE TABLE ecommerce.tags_products (
id SERIAL PRIMARY KEY,
product_id INT NOT NULL,
tag_id INT NOT NULL, 
FOREIGN KEY (product_id) REFERENCES ecommerce.products(id) ON DELETE CASCADE,
FOREIGN KEY (tag_id) REFERENCES ecommerce.tags(id) ON DELETE CASCADE,
UNIQUE(product_id, tag_id)
)

CREATE TABLE ecommerce.carts (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
date_creation DATE DEFAULT CURRENT_DATE,
date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES ecommerce.users(id) ON DELETE CASCADE

)

-- talbe cart_products
CREATE TABLE ecommerce.cart_products (
id SERIAL PRIMARY KEY,
cart_id INT NOT NULL,
product_id INT NOT NULL,
quantite INT NOT NULL,
date_ajout DATE DEFAULT CURRENT_DATE,
FOREIGN KEY (cart_id) REFERENCES ecommerce.carts(id) ON DELETE CASCADE,
FOREIGN KEY (product_id) REFERENCES ecommerce.products(id) ON DELETE CASCADE,
UNIQUE(cart_id, product_id)
)

-- table ordre 
-- avec la contriante de vérification de status 
CREATE TABLE ecommerce.orders (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
status VARCHAR (20) DEFAULT 'pending',
total_amount decimal (10, 2),
created_at DATE DEFAULT CURRENT_DATE,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES ecommerce.users(id) ON DELETE CASCADE,
CONSTRAINT check_status CHECK (status IN('pending', 'delivered', 'cancelled'))
-- CONSTRAINT  check_status CHECK( status IN ('ok', 'en panne', 'maintenance'))
)

-- table order items 
CREATE TABLE ecommerce.order_items (
id SERIAL PRIMARY KEY,
order_id INT NOT NULL,
product_id INT NOT NULL,
quantity INT NOT NULL CHECK (quantity > 0),
unit_price DECIMAL (10,2) NOT NULL,
FOREIGN KEY (product_id) REFERENCES ecommerce.products(id) ON DELETE CASCADE,
FOREIGN KEY (order_id) REFERENCES ecommerce.orders(id) ON DELETE CASCADE
)

-- TABLE orders adres 
CREATE TABLE ecommerce.order_addresses (
id SERIAL PRIMARY KEY,
order_id INT NOT NULL UNIQUE,
street varchar (100) not null,
city varchar (50) NOT NULL,
postal_code VARCHAR (10) NOT NULL,
country varchar (40) NOT NULL,
created_at DATE DEFAULT CURRENT_DATE,
FOREIGN KEY (order_id) REFERENCES ecommerce.orders(id) ON DELETE CASCADE
)

-- table notifications 
CREATE TABLE ecommerce.notifications (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
title VARCHAR (100) NOT NULL,
notification_type varchar (20) DEFAULT ('info') ,
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES ecommerce.users(id) ON DELETE CASCADE,
CONSTRAINT check_notification_type CHECK (notification_type IN ('info', 'alert', 'error'))
)

