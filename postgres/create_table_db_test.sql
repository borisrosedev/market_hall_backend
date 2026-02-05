-- CREATE TABLE categories (
-- id SERIAL PRIMARY KEY,
-- title VARCHAR (150) NOT NULL,
-- description TEXT
-- );

-- INSERT INTO categories (title, description) VALUES ('Plat', 'Desert'),  ('Supe', 'Gateau') ;

-- CREATE TABLE recipes (
-- id SERIAL PRIMARY KEY ,
-- title VARCHAR (150),
-- slug VARCHAR (50),
-- contents TEXT,
-- categorie_id int ,
-- FOREIGN KEY (categorei_id) REFERENCES categories(id)
-- )

-- CREAT

-- SELECT * from categories 

-- INSERT INTO recipes (title, slug, categorie_id) VALUES ('Créem', 'Créem_anglias', 1)

-- SELECT * FROM recipes r JOIN categories c on r.categorie_id = c.id 
DROP TABLE IF EXISTS "users";
DROP TABLE IF EXISTS "recipes";


CREATE TABLE users (
id SERIAL PRIMARY KEY ,
username VARCHAR (150) UNIQUE NOT NULL,
email VARCHAR (180) UNIQUE NOT NULL
);
CREATE TABLE recipes (
id SERIAL PRIMARY KEY, 
title VARCHAR (150) NOT NULL,
slug VARCHAR (150),
created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
duration INT DEFAULT 0 NOT NULL,
user_id INT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)

CREATE TABLE categories (
id serial PRIMARY KEY,
title VARCHAR (150) not null,
)

CREATE TABLE categories_recipes (
recipe_id INT,
categorie_id INT, 
FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
FOREIGN KEY (categorie_id) REFERENCES categories(id) ON DELETE CASCADE,
PRIMARY KEY (recipe_id, categorie_id),
UNIQUE (recipe_id, categorie_id)
)

-- INGREDIENTS 
CREATE TABLE ingredients (
id SERIAL PRIMARY KEY,
nom VARCHAR (150)
);

-- INGREDIENTS_RECIPES 
CREATE TABLE ingredients_recipes (
recipe_id INT NOT NULL,
ingredient_id INT NOT NULL,
quantity INT,
unit VARCHAR (20),
FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
PRIMARY KEY (recipe_id, ingredient_id),
UNIQUE (recipe_id, ingredient_id)
)

