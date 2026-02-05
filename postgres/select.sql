-- alter avec les les mots clés importants 
-- Ajouter une colonne 
ALTER TABLE users ADD COLUMN phone VARCHAR(15)

-- Renemer une colonne
ALTER TABLE commande RENAME COLUMN statut TO status

-- alter un chiffre decimal
ALTER TABLE products ALTER COLUMN price TYPE DECIMAL(15, 2)

-- pour ajouter des conditions dauns une colonne existante 
ALTER TABLE users ALTER COLUMN email SET NOT NULL

-- Les notions a retenire, ADD, RENAME, ALTER




-- SELECT 
SELECT * FROM ecommerce.users ORDER BY nom DESC

-- voires tous les utilisateurs 
SELECT nom, prenom, COUNT(*) AS nomes_utilisateurs FROM ecommerce.users
GROUP BY nom, prenom

-- voir tous les produits 
SELECT nom, prix, date_creation, COUNT(*) FROM ecommerce.products
GROUP BY nom, prix, date_creation

-- conter les nombres des produits qui coute plus d'un certiant prix 
SELECT nom, prix, COUNT(*) AS nombres_produits FROM ecommerce.products
WHERE prix > 400
GROUP BY nom, prix

-- compter les produits de chaque catergorie 
SELECT t.nom AS categorei, COUNT(p.id) AS nombre_produits
FROM ecommerce.products p 
GROUP BY  t.id ,t.nom 


-- prix total de tous les produits 
SELECT SUM(prix) AS prix_total 
FROM ecommerce.products

-- Les commandes avec les noms des utilisateurs 
SELECT o.total_amount,o.status, o.id AS commande_id, u.nom AS nom_client, u.prenom
FROM ecommerce.orders o
JOIN ecommerce.users u ON o.user_id = u.id

-- faire un lefjoin pour avoir tous les colones meme les nulles 
SELECT o.total_amount, u.nom, o.id 
FROM ecommerce.users u 
LEFT JOIN ecommerce.orders o ON u.id = o.user_id


-- voir tous les procuits avec les prix 
SELECT nom, prix, stock FROM ecommerce.products 
-- voir les produits et leurs tags 
SELECT p.nom, p.prix t.nom AS categorie FROM ecommerce.products p JOIN ecommerce.tags_products tp = tp.product_id

-- voir les commandes avec les noms des clients 
SELECT u.nom, u.prenom, o.order_id, o.status FROM ecommerce.users u JOIN ecommerce.orders o 
INNER JOIN ecommerce.users u ON o.user_id = o.user_id

 -- Aggregate Functions
SELECT COUNT(*) FROM ecommerce.products 

SELECT MAX(prix), MIN(prix), AVG (prix) FROM ecommerce.products 




SELECT max(prix) FROM ecommerce.products
SELECT COUNT(*) AS nb_produits
FROM ecommerce.products

SELECT * FROM ecommerce.table_structure

SELECT t.nom, COUNT(*) AS nb_produits 
FROM ecommerce.tags t
JOIN ecommerce.tags_products tp ON t.id = tp.tag_id 
group by t.nom 

SELECT 
    o.id,
    u.nom,
    u.prenom,
    o.status,
    o.total_amount
FROM ecommerce.orders o LEFT JOIN ecommerce.users u ON o.id = o.user_id

-- afficher le nom et le prix de produit avec son tag 
SELECT p.nom, p.unit_price, t.nom AS categorie 
FROM ecommerce.products p
INNER JOIN ecommerce.tags_products tp ON  ecommerce.products c

-- afficher les commandes d'un utilisateur 
SELECT o.total_amount, u.nom
FROM ecommerce.orders o 
JOIN ecommerce.users u ON o.user_id = u.id 

-- afficher les produits d'une commande 
SELECT p.nom, o.id 
FROM ecommerce.orders o 
JOIN ecommerce.order_items oi ON o.id = io.order_id
JOIN ecommerce.oi.product_id = p.id

-- afficher les tages d'un produits 
SELECT t.nom, p.nom
FROM ecommerce.products p
JOIN ecommerce.tags_products tp ON p.id = tp.product_id
JOIN ecommerce.tags t ON tp.tag_id = t.id;
