-- insertion 
-- insert tags 
INSERT INTO ecommerce.tags (nom, description) VALUES ('Electronics', 'Electronic products'),
    ('Clothing', 'Clothes and accessories'),
    ('Books', 'Books and literature');

-- insert products 
INSERT INTO ecommerce.products (nom, description, prix, stock) VALUES ('MacOS', 'Performante', 545.23, 12),
('Windows', 'Facile à utiliser', 350.23, 30), ('Linux', 'Agérable', 454.23, 40),

-- INSERT dans la tag_product
INSERT INTO ecommerce.tags_products (product_id, tag_id) VALUES (1, 1),
    (1, 2),
    (1, 3),
    (3, 3);

-- user cart
insert into ecommerce.carts (user_id) VALUES (1), (2)

-- carts products 
INSERT INTO ecommerce.cart_products (cart_id, product_id, quantite) VALUES (1, 1, 1), (1, 2, 2)

-- order 
INSERT INTO ecommerce.orders (user_id, status, total_amount)  VALUES (1, 'pending', 856.12)

-- order items 
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) VALUES (2, 1, 2, 562.41)

-- order addresses 
INSERT INTO ecommerce.order_addresses (order_id, street, city, postal_code, country ) VALUES (2, 'rue de mayenne', 'mayenne', '53100', 'France')

-- notifications 
INSERT INTO ecommerce.notifications (user_id, title, notification_type) VALUES (1, 'Message de teste', 'error' )

-- opérations de boolean 
-- TRUE AND TRUE = TRUE 
-- TRUE AND FALSE = FALSE 
-- FALSE AND FALSE = FALSE 

-- TRUE OR FALSE = TRUE
-- FALSE OR TRUE = TRUE 
-- TRUE OR FALSE = TRUE 
-- FALSE OR FALSE = FALSE 

-- Pour expliquer une requete comment s'excute 
EXPLAIN select * from ecommerce.users where id = 1 





