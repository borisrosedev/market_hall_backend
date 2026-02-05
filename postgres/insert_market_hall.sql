-- =====================================================
-- MARKET HALL - INSERTION DE DONNÉES RÉALISTES
-- =====================================================

-- =====================================================
-- 1. INSÉRER LES UTILISATEURS
-- =====================================================

INSERT INTO ecommerce.users (nom, prenom, email, mdp, telephone) 
VALUES 
('Dupont', 'Ahmed', 'ahmed.dupont@gmail.com', 'hash_password_1', '0612345678'),
('Martin', 'Fatima', 'fatima.martin@gmail.com', 'hash_password_2', '0687654321'),
('Bernard', 'Hassan', 'hassan.bernard@gmail.com', 'hash_password_3', '0698765432'),
('Leclerc', 'Sophie', 'sophie.leclerc@gmail.com', 'hash_password_4', '0677889900'),
('Moreau', 'Pierre', 'pierre.moreau@gmail.com', 'hash_password_5', '0666774455');
-- =====================================================
-- 2. INSÉRER LES CATÉGORIES (TAGS)
-- =====================================================

INSERT INTO ecommerce.tags (nom, description) 
VALUES 
('Systèmes d''exploitation', 'Systèmes d''exploitation pour ordinateurs'),
('Productivité', 'Outils de productivité et bureautique'),
('Sécurité', 'Logiciels de sécurité et antivirus'),
('Développement', 'Outils de développement et IDE'),
('Gratuit', 'Logiciels gratuits et open-source'),
('Premium', 'Logiciels premium et payants');

-- =====================================================
-- 3. INSÉRER LES PRODUITS
-- =====================================================

INSERT INTO ecommerce.products (nom, description, prix, stock) 
VALUES 
('MacOS Ventura', 'Système d''exploitation Apple haute performance', 999.99, 5),
('Windows 11 Pro', 'Système d''exploitation Microsoft professionnel', 199.99, 15),
('Ubuntu 22.04', 'Distribution Linux gratuite et open-source', 0.00, 100),
('Microsoft Office 365', 'Suite bureautique complète (Word, Excel, PowerPoint)', 69.99, 20),
('LibreOffice', 'Suite bureautique gratuite et open-source', 0.00, 50),
('Norton AntiVirus', 'Logiciel antivirus premium', 49.99, 12),
('Visual Studio Code', 'Éditeur de code gratuit pour développeurs', 0.00, 200),
('JetBrains IntelliJ IDEA', 'IDE professionnel pour développement Java', 199.99, 8),
('Figma', 'Outil de design collaboratif en ligne', 12.99, 30),
('Adobe Creative Cloud', 'Suite complète Photoshop, Illustrator, Premiere', 54.99, 10);

-- =====================================================
-- 4. LIER LES PRODUITS AUX CATÉGORIES (TAGS_PRODUCTS)
-- =====================================================

INSERT INTO ecommerce.tags_products (product_id, tag_id) 
VALUES 
-- MacOS
(2, 2),  -- Systèmes d'exploitation
(1, 6),  -- Premium

-- Windows 11
(2, 1),  -- Systèmes d'exploitation
(2, 6),  -- Premium

-- Ubuntu
(3, 1),  -- Systèmes d'exploitation
(3, 5),  -- Gratuit

-- Microsoft Office 365
(4, 2),  -- Productivité
(4, 6),  -- Premium

-- LibreOffice
(5, 2),  -- Productivité
(5, 5),  -- Gratuit

-- Norton AntiVirus
(6, 3),  -- Sécurité
(6, 6),  -- Premium

-- VS Code
(7, 4),  -- Développement
(7, 5),  -- Gratuit

-- IntelliJ IDEA
(8, 4),  -- Développement
(8, 6),  -- Premium

-- Figma
(9, 2),  -- Productivité
(9, 4),  -- Développement
(9, 6),  -- Premium

-- Adobe Creative Cloud
(10, 4), -- Développement
(10, 6); -- Premium

-- =====================================================
-- 5. INSÉRER LES PANIERS (CARTS)
-- =====================================================
INSERT INTO ecommerce.carts (user_id) 
VALUES 
(1),  -- Ahmed a un panier
(2),  -- Fatima a un panier
(3),  -- Hassan a un panier
(4);  -- Sophie a un panier

-- =====================================================
-- 6. AJOUTER DES PRODUITS AUX PANIERS (CART_PRODUCTS)
-- =====================================================

-- Panier d'Ahmed (user_id = 1)
INSERT INTO ecommerce.cart_products (cart_id, product_id, quantite) 
VALUES 
(1, 1, 1),  -- 1 MacOS
(1, 4, 2);  -- 2 Office 365

-- Panier de Fatima (user_id = 2)
INSERT INTO ecommerce.cart_products (cart_id, product_id, quantite) 
VALUES 
(2, 7, 1),  -- 1 VS Code
(2, 9, 1);  -- 1 Figma

-- Panier de Hassan (user_id = 3)
INSERT INTO ecommerce.cart_products (cart_id, product_id, quantite) 
VALUES 
(3, 2, 1),  -- 1 Windows 11
(3, 6, 1);  -- 1 Norton

-- Panier de Sophie (user_id = 4)
INSERT INTO ecommerce.cart_products (cart_id, product_id, quantite) 
VALUES 
(4, 10, 1); -- 1 Adobe Creative Cloud

-- =====================================================
-- 7. INSÉRER LES COMMANDES (ORDERS)
-- =====================================================
??????
INSERT INTO ecommerce.orders (user_id, status, total_amount) 
VALUES 
-- Commandes d'Ahmed
(1, 'cancelled', 1139.97),  -- 1 MacOS (999.99) + 2 Office (69.99 * 2)
(1, 'pending', 199.99),  -- 1 Windows 11

-- Commandes de Fatima
(2, 'cancelled', 82.98),    -- 1 VS Code (0) + 1 Figma (12.99)
(2, 'delivered', 49.99),       -- 1 Norton

-- Commandes de Hassan
(3, 'cancelled', 249.98),   -- 1 Windows (199.99) + 1 Norton (49.99)

-- Commandes de Sophie
(4, 'pending', 54.99),   -- 1 Adobe Creative Cloud

-- Commandes de Pierre (user_id = 5)
(5, 'cancelled', 199.99);   -- 1 IntelliJ IDEA

-- SELECT constraint_name, check_clause
-- FROM information_schema.check_constraints
-- WHERE constraint_name LIKE '%status%' OR constraint_name LIKE '%statut%';

-- =====================================================
-- 8. AJOUTER LES ARTICLES DES COMMANDES (ORDER_ITEMS)
-- =====================================================
SELECT * from ecommerce.orders
DELETE FROM ecommerce.orders;
ALTER SEQUENCE ecommerce.orders_id_seq RESTART WITH 1;



-- Commande 1 (Ahmed - MacOS + Office)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(1, 1, 1, 999.99),  -- 1 MacOS
(1, 4, 2, 69.99);   -- 2 Office 365

-- Commande 2 (Ahmed - Windows 11)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(2, 2, 1, 199.99);  -- 1 Windows 11

-- Commande 3 (Fatima - VS Code + Figma)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(3, 7, 1, 0.00),    -- 1 VS Code (gratuit)
(3, 9, 1, 12.99);   -- 1 Figma

-- Commande 4 (Fatima - Norton)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(4, 6, 1, 49.99);   -- 1 Norton

-- Commande 5 (Hassan - Windows + Norton)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(5, 2, 1, 199.99),  -- 1 Windows 11
(5, 6, 1, 49.99);   -- 1 Norton

-- Commande 6 (Sophie - Adobe)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(6, 10, 1, 54.99);  -- 1 Adobe Creative Cloud

-- Commande 7 (Pierre - IntelliJ)
INSERT INTO ecommerce.order_items (order_id, product_id, quantity, unit_price) 
VALUES 
(7, 8, 1, 199.99);  -- 1 IntelliJ IDEA

-- =====================================================
-- 9. AJOUTER LES ADRESSES DE LIVRAISON (ORDER_ADDRESSES)
-- =====================================================

INSERT INTO ecommerce.order_addresses (order_id, street, city, postal_code, country) 
VALUES 
(4, '321 Rue Montmartre', 'Paris', '75009', 'France'),
(5, '654 Rue de Rivoli', 'Paris', '75004', 'France'),
(6, '987 Avenue Foch', 'Paris', '75016', 'France'),
(7, '111 Rue du Faubourg Saint-Honoré', 'Paris', '75008', 'France');

-- =====================================================
-- 10. AJOUTER DES NOTIFICATIONS (NOTIFICATIONS)
-- =====================================================

SELECT 
    constraint_name,
    check_clause
FROM information_schema.check_constraints;

INSERT INTO ecommerce.notifications (user_id, title, notification_type, is_read) 
VALUES 
-- Notifications d'Ahmed
(1, 'Commande #1 confirmée', 'alert', false),
(1, 'Commande #1 expédiée', 'alert', true),
(1, 'Commande #2 en attente de paiement', 'alert', false),

-- Notifications de Fatima
(2, 'Commande #3 confirmée', 'alert', true),
(2, 'Commande #4 livrée', 'alert', true),
(2, 'Nouvelle promotion: -20% sur les outils dev', 'info', false),

-- Notifications de Hassan
(3, 'Commande #5 confirmée', 'alert', false),
(3, 'Rupture de stock: Windows 11', 'alert', true),

-- Notifications de Sophie
(4, 'Commande #6 en attente de paiement', 'alert', false),
(4, 'Bienvenue chez Market Hall!', 'info', true),

-- Notifications de Pierre
(5, 'Commande #7 confirmée', 'alert', false),
(5, 'Invitation: Rejoignez notre programme VIP', 'info', false);

-- =====================================================
-- VÉRIFICATION DES DONNÉES INSÉRÉES
-- =====================================================

-- Vérifier le nombre d'utilisateurs
-- SELECT COUNT(*) AS total_utilisateurs FROM ecommerce.users;

-- Vérifier le nombre de produits
-- SELECT COUNT(*) AS total_produits FROM ecommerce.products;

-- Vérifier le nombre de commandes
-- SELECT COUNT(*) AS total_commandes FROM ecommerce.orders;

-- Vérifier le nombre d'articles commandés
-- SELECT COUNT(*) AS total_articles FROM ecommerce.order_items;

-- Afficher toutes les commandes avec les montants
-- SELECT id, user_id, status, total_amount FROM ecommerce.orders ORDER BY id;

-- =====================================================
-- VIDER TOUTES LES TABLES (dans le bon ordre)
-- =====================================================

-- IMPORTANT : Supprimer en respectant les clés étrangères !
-- Les tables "enfants" d'abord, puis les tables "parents"

-- 1. Supprimer les notifications (référence users)
DELETE FROM ecommerce.notifications;

-- 2. Supprimer les articles de commande (référence orders et products)
DELETE FROM ecommerce.order_items;

-- 3. Supprimer les adresses de commande (référence orders)
DELETE FROM ecommerce.order_addresses;

-- 4. Supprimer les commandes (référence users)
DELETE FROM ecommerce.orders;

-- 5. Supprimer les produits du panier (référence carts et products)
DELETE FROM ecommerce.cart_products;

-- 6. Supprimer les paniers (référence users)
DELETE FROM ecommerce.carts;

-- 7. Supprimer les relations produits-tags (référence products et tags)
DELETE FROM ecommerce.tags_products;

-- 8. Supprimer les produits (pas de référence, mais avant les users)
DELETE FROM ecommerce.products;

-- 9. Supprimer les catégories (pas de référence, mais avant les users)
DELETE FROM ecommerce.tags;

-- 10. Supprimer les utilisateurs (derniers, car beaucoup les référencent)
DELETE FROM ecommerce.users;

-- =====================================================
-- RÉINITIALISER LES SÉQUENCES (pour que les IDs recommencent à 1)
-- =====================================================

ALTER SEQUENCE ecommerce.users_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.tags_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.products_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.tags_products_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.carts_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.cart_products_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.orders_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.order_items_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.order_addresses_id_seq RESTART WITH 1;
ALTER SEQUENCE ecommerce.notifications_id_seq RESTART WITH 1;

-- =====================================================
-- VÉRIFICATION
-- =====================================================

-- Vérifier que tout est vide
-- SELECT COUNT(*) AS users FROM ecommerce.users;
-- SELECT COUNT(*) AS products FROM ecommerce.products;
-- SELECT COUNT(*) AS orders FROM ecommerce.orders;
-- SELECT COUNT(*) AS notifications FROM ecommerce.notifications;