DROP DATABASE IF EXISTS restaurant_App;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS restaurant_App;

-- Utilisation de cette base de donnée

USE restaurant_App;

-- TABLE DE BASE

create table t_plats (
    id_plat int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    plat_nom varchar(60) NOT NULL,
    plat_type varchar(10) NOT NULL,
    plat_est_chaud varchar(5) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_restaurants (
    id_restaurant int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    restaurant_nom varchar(60) NOT NULL,
    restaurant_type varchar(60) NOT NULL,
    FK_pays int(11) NULL,
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
    prix_type varchar(14) NOT NULL,
    prix_valeur float NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table t_ingredients (
    id_ingredient int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ingredient_nom varchar(60) NOT NULL,
    ingredient_est_sucre varchar(5) NOT NULL,
    provenance_est_bio varchar(3) NOT NULL,
    categorie_type varchar(25)NOT NULL,
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
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Jambon', 'salé', 'non', 'Charcuteries', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Poulet', 'salé', 'non', 'Viandes', '6');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Viande haché boeuf', 'salé', 'non', 'Viandes', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Sucre', 'sucré', 'non', 'Sucres et produits sucrés', '6');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Lait', 'sucré', 'oui', 'Lait', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Saumon', 'salé', 'non', 'Poissons', '16');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Pomme', 'sucré', 'oui', 'Fruits', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Poire', 'sucré', 'oui', 'Fruits', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Oeuf', 'salé', 'oui', 'Oeufs', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Haricot', 'salé', 'non', 'Légumineuses', '7');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Miel', 'sucré', 'non', 'Sucres et produits sucrés', '1');
INSERT INTO `restaurant_app`.`t_ingredients` (`ingredient_nom`, `ingredient_est_sucre`, `provenance_est_bio`, `categorie_type`, `FK_pays`) VALUES ('Chocolat', 'sucré', 'non', 'Sucres et produits sucrés', '1');
-- Insert Plats 
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('petit salad\'bar', 'entree', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('grand salad\'bar', 'entree', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('salade oceane', 'entree', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('salade crunchy chicken:', 'entree', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Saucisse de veau grillé, légumes rôtis et pomme purée', 'plat', 'chaud');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Sauté de boeuf Choux rouges braisés Pomme purée maison', 'plat', 'chaud');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Gratin de gnocchi aux légumes', 'plat', 'chaud');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Cuisse de poulet confit au citron', 'plat', 'chaud');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Focaccia Chorizo et pesto', 'plat', 'chaud');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Tiramisu', 'dessert', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Tartelette aux fruits du jour', 'dessert', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('Verrine gourmande du jour', 'dessert', 'froid');
INSERT INTO `restaurant_app`.`t_plats` (`plat_nom`, `plat_type`, `plat_est_chaud`) VALUES ('ella’s cheesecake', 'dessert', 'froid');
-- Insert into table particularite
INSERT INTO `restaurant_app`.`t_particularites` (`particularite_genre`) VALUES ('sans gluten');
INSERT INTO `restaurant_app`.`t_particularites` (`particularite_genre`) VALUES ('sans lactose');
INSERT INTO `restaurant_app`.`t_particularites` (`particularite_genre`) VALUES ('végétarien');
INSERT INTO `restaurant_app`.`t_particularites` (`particularite_genre`) VALUES ('végan');
INSERT INTO `restaurant_app`.`t_particularites` (`particularite_genre`) VALUES ('sans porc');
-- Insert into table prix
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Etudiant','8.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Etudiant','12.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Etudiant','6.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Etudiant','7.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Etudiant','9.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Doctorant','13.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Doctorant','12.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Doctorant','11.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Doctorant','14.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Campus','11.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Campus','9.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Campus','10.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Campus','8.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Externe','15.0');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Externe','15.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Externe','17.50');
INSERT INTO `restaurant_app`.`t_prix` (`prix_type`, `prix_valeur`) VALUES ('Externe','14.50');

-- Insert into table de liaison(plat-particularité)
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('1', '1', '1');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('2', '1', '3');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('3', '1', '4');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('4', '1', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('5', '2', '1');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('6', '2', '3');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('7', '2', '4');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('8', '2', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('9', '3', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('10', '4', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('11', '5', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('12', '6', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('13', '7', '4');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('14', '7', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('15', '8', '2');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('16', '8', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('17', '9', '4');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('18', '9', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('19', '10', '4');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('20', '10', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('21', '11', '2');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('22', '11', '3');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('23', '11', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('24', '12', '2');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('25', '12', '3');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('26', '12', '5');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('27', '13', '2');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('28', '13', '3');
INSERT INTO `restaurant_app`.`t_plats_particularites` (`id_plat_particularite`, `FK_plat`, `FK_particularite`) VALUES ('29', '13', '5');