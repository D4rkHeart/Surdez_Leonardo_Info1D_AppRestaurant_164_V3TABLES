DROP DATABASE IF EXISTS restaurant_App;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS restaurant_App;

-- Utilisation de cette base de donnée

USE restaurant_App;

-- TABLE DE BASE

create table t_plats (
    id_plat int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plat_nom varchar(60) NOT NULL,
    plat_type ENUM("entree","plat","dessert") NOT NULL,
    plat_est_chaud boolean NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_restaurants (
    id_restaurant int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    restaurant_nom varchar(60) NOT NULL,
    restaurant_type ENUM("Fine Dining","Casual Dining","Fast Casual","Ghost Restaurant","Fast Food", "Food Truck","Cafe","Buffet", "Cafeteria","Coffee House") NOT NULL,
    FK_pays int(11) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_particularites (
    id_particularite int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    particularite_genre varchar(60)  NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_prix (
    id_prix int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    prix_type ENUM("Étudiant/Apprenti","Doctorant","Visiteur","Campus","Général") NOT NULL,
    prix_valeur float NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_ingredients (
    id_ingredient int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ingredient_nom varchar(60) NOT NULL,
    ingredient_est_sucre boolean NOT NULL,
    provenance_est_bio boolean NOT NULL,
    categorie_type ENUM("Légumes","Fruits","Viandes","Charcuteries","Poissons ","OEufs","Produits laitiers","Lait","Fromages","Matières grasses","Matières grasses d’origine animale","Huiles et margarines","Céréales et dérivés","Légumineuses","Sucres et produits sucrés") NOT NULL,
    FK_pays int(11) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_pays (
  id_pays int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom varchar(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- Insert into t_plats values (NULL,"Tiramisu","dessert", true);

-- JOIN TABLE
CREATE TABLE t_plats_particularites (
  id_plat_particularite int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  FK_plat int(11) NOT NULL,
  FK_particularite int(11) NOT NULL,
  UNIQUE INDEX `id_plat_particularite_UNIQUE` (`id_plat_particularite` ASC)
);

CREATE TABLE t_plats_coutent_prix (
  id_plat_coute_prix int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  FK_plat int(11) NOT NULL,
  FK_prix int(11) NOT NULL
);

CREATE TABLE t_plats_contients_ingredients (
  id_plat_contient_ingredient int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  FK_plat int(11) NOT NULL,
  FK_ingredient int(11) NOT NULL
);

-- Insert Into --
-- Insert nom
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Suisse');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Italie');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('USA');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Allemagne');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('France');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Brésil');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Chili');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Méxique');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Espagne');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Liban');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Chine');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Inde');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Thaïlande');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Turc');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Japon');
INSERT INTO `restaurant_app`.`t_pays` (`nom`) VALUES ('Norvège');


-- Insert restaurant
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Holy cow', 'Fast Food', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Hong Thaï Rung', 'Food Truck', '13');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Maharaja', 'Food Truck', '12');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Li Beirut', 'Food Truck', '10');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Soleil', 'Food Truck', '14');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Fleur de Pains', 'Food Truck', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Espace Copernic', 'Fine Dining', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Montreux Jazz Café', 'Casual Dining', '3');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('La Table de Vallotton', 'Fine Dining', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Gina Ristorante', 'Fine Dining', '2');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Food Lab – Alpine', 'Buffet', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Foodlab Native', 'Buffet', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Hopper', 'Cafeteria', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('Piano', 'Buffet', '1');
INSERT INTO `restaurant_app`.`t_restaurants` (`restaurant_nom`, `restaurant_type`, `FK_pays`) VALUES ('L’Ornithorynque', 'Buffet', '15');
-- Insert Ingrédient 
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Jambon', '0', '0', 'Charcuteries', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Poulet', '0', '0', 'Viandes', '6');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Viande haché boeuf', '0', '0', 'Viandes', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Sucre', '1', '0', 'Sucres et produits sucrés', '6');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Lait', '1', '1', 'Lait', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Saumon', '0', '0', 'Poissons', '16');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Pomme', '1', '1', 'Fruits', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Poire', '1', '1', 'Fruits', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Oeuf', '0', '1', 'Oeufs', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Haricot', '0', '0', 'Légumineuses', '7');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Miel', '1', '0', 'Sucres et produits sucrés', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Chocolat', '1', '0', 'Sucres et produits sucrés', '1');
-- Insert Plats 
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('petit salad\'bar', 'entree', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('grand salad\'bar', 'entree', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('salade oceane', 'entree', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('salade crunchy chicken:', 'entree', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Saucisse de veau grillé, légumes rôtis et pomme purée', 'plat', '1');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Sauté de boeuf Choux rouges braisés Pomme purée maison', 'plat', '1');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Gratin de gnocchi aux légumes', 'plat', '1');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Cuisse de poulet confit au citron', 'plat', '1');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Focaccia Chorizo et pesto', 'plat', '1');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Tiramisu', 'dessert', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Tartelette aux fruits du jour', 'dessert', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Verrine gourmande du jour', 'dessert', '0');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('ella’s cheesecake', 'dessert', '0');

