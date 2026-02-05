
-- RÉSUMÉ POUR LES CONCEPTS POSTGRESQL APPRIS


-- 1. CRÉER UNE BASE DE DONNÉES
CREATE DATABASE ma_base;

-- 2. SE CONNECTER À LA BASE
-- \c ma_base VIA CMD OU powersehll

-- 3. CRÉER UN SCHÉMA (ce que j'ai compris c'est comme un dossier qui contien )
CREATE SCHEMA mon_schema; -- 



-- TABLE AVEC TOUS LES CONCEPTS IMPORTANTS
CREATE TABLE mon_schema.ma_table (
    -- 1. PRIMARY KEY : clé primaire (identifiant unique)
    id SERIAL PRIMARY KEY, -- le concept SERIAL je vois la première fois
    
    -- 2. VARCHAR : texte avec limite de caractères
    nom VARCHAR(50) NOT NULL,
    
    -- 3. NOT NULL : valeur obligatoire
    prenom VARCHAR(50) NOT NULL,
    
    -- 4. UNIQUE : valeur unique 
    email VARCHAR(100) UNIQUE NOT NULL,
    
    -- 5. TIMESTAMP : date + heure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 6. DATE : seulement la date
    date_inscription DATE DEFAULT CURRENT_DATE,
    
    -- 7. DECIMAL : nombres avec décimales
    prix DECIMAL(10, 2),
    
    -- 8. INT : nombre entier
    quantite INT NOT NULL,
    
    -- 9. BOOLEAN : vrai/faux
    est_actif BOOLEAN DEFAULT TRUE,
    
    -- 10. CHECK contrainte pour la vérification 
    CONSTRAINT check_prix CHECK (prix > 0),
    CONSTRAINT check_quantite CHECK (quantite >= 0),
    CONSTRAINT check_statut CHECK (statut IN ('en_cours', 'ok', 'confirmée'))
);

-- Tables avec des clés étrangères  

CREATE TABLE mon_schema.table_association (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT
);

-- Table avec clé étrangère qui fait la référence à une autre table 
CREATE TABLE mon_schema.commande (
    id SERIAL PRIMARY KEY,
    
    -- FOREIGN KEY : lien avec une autre table
    association_id INT NOT NULL,
    
    -- ON DELETE CASCADE : si l'association est supprimée, supprime aussi la commande
    FOREIGN KEY (association_id) REFERENCES mon_schema.table_association(id) ON DELETE CASCADE,
    
    statut VARCHAR(20) DEFAULT 'en_attente',
    montant DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE AVEC RELATION PLUSIEURS-À-PLUSIEURS

-- Table d'association (pont entre deux tables)
CREATE TABLE mon_schema.produits_categories (
    id SERIAL PRIMARY KEY,
    produit_id INT NOT NULL,
    categorie_id INT NOT NULL,
    
    -- UNIQUE sur plusieurs colonnes : empêche les doublons
    UNIQUE(produit_id, categorie_id),
    
    FOREIGN KEY (produit_id) REFERENCES mon_schema.produits(id) ON DELETE CASCADE,
    FOREIGN KEY (categorie_id) REFERENCES mon_schema.categories(id) ON DELETE CASCADE
);

-- INSERTION DES DONNÉES

-- INSERT : ajouter des données
INSERT INTO mon_schema.table_association (nom, description) 
VALUES ('Association 1', 'Description');

-- INSERT  ajouter plusieurs enregistrements à la fois
INSERT INTO mon_schema.commande (association_id, statut, montant) 
VALUES 
(1, 'en_attente', 99.99),
(1, 'confirmee', 149.99),
(1, 'livree', 199.99);

-- MODIFICATION DE DONNÉES

-- UPDATE : modifier des enregistrements 
UPDATE mon_schema.commande 
SET statut = 'confirmee' 
WHERE id = 1;


-- SUPPRESSION DE DONNÉES

-- DELETE : supprimer des enregistrements
DELETE FROM mon_schema.commande 
WHERE statut = 'annulee';

-- SELECT simple : afficher toutes les données
SELECT * FROM mon_schema.commande;

-- SELECT avec colonnes spécifiques
SELECT id, statut, montant FROM mon_schema.commande;

-- SELECT avec WHERE : filtrer
SELECT * FROM mon_schema.commande WHERE statut = 'confirmee';

-- SELECT avec ORDER BY : trier
SELECT * FROM mon_schema.commande ORDER BY montant DESC;



-- VOIR LA STRUCTURE DES TABLES
-- Voir la structure d'une table
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'mon_schema' 
AND table_name = 'ma_table';

-- Voir toutes les tables du schéma
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'mon_schema';




-- Utiliser la VIEW
SELECT * FROM mon_schema.commandes_confirmees;


-- types de données que j'ia utilisés pour la création des tables 
-- VARCHAR(n)      : texte limité à n caractères
-- TEXT            : texte illimité
-- INT             : nombre entier
-- DECIMAL(10,2)   : nombre avec décimales 10 chiffres, 2 après la virgule
-- DATE            : date uniquement YYYY-MM-DD
-- TIMESTAMP       : date et heure
-- BOOLEAN         : TRUE/FALSE
-- SERIAL          : nombre auto-incrémenté

-- commandes sql quand on se connecte via cmd 
-- \c database_name        : se connecter à une base
-- \l                      : lister les bases
-- \q                      : quitter psql


