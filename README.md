# Module 164 2022.06.10
#####By D4rkHeart

---

### Voici les étapes afin de télécharger et modifier ce CRUD (Create Read Update Delete) 

### Serveur local Mysql
* Un serveur MySql doit être installé
  * UWAMP : sur le site de "UWAMP", lire "Prerequisites IMPORTANT!!" (vous devez installer une des distributions Visual C++, j'ai choisi la plus récente) 
  * UWAMP : installer la version "EXE" (Choisir : Télécharger Exe/Install) est préférable à la version "PORTABLE"
  * UWAMP : accepter les 2 alertes de sécurité d'accès aux réseaux (apache et MySql)
  * MAC : MAMP ou https://www.codeur.com/tuto/creation-de-site-internet/version-mysql/
  * Contrôler que tout fonctionne bien. Ouvrir "UWAMP". Cliquer sur le bouton "PhpMyAdmin". Utilisateur : root Mot de passe : root
### Language : Python
* Python doit être installé.
  * ATTENTION : Cocher la case pour que le "PATH" intègre le programme Python
  * Une fois la "case à cocher" du PATH cochée, il faut choisir d'installer
  * Un peu avant la fin du processus d'intallation, cliquer sur "disabled length limit" et cliquer sur "CLOSE"
  * Le test de Python se fait après avec le programme "PyCharm"

#### IDE : Pycharm 
* "PyCharm" (community) doit être intallé.
  * Lors de l'installation, il faut cocher toutes les options ASSOCIATIONS, ADD PATH, etc
  * Ouvrir "PyCharm" pour la première fois pour le configurer. Choisir le bouton "New Project"
  * Changer le répertoire pour ce nouveau projet, il faut créer un nouveau répertoire "vide" dans votre ordi en local.
  * Il est important d'avoir sélectionné le répertoire que vous venez de créer car "PyCharm" va automatiquement créer un
    environnement virtuel (venv) dans ce répertoire
  * Menu : File->Settings->Editor->General->Auto Import (rubrique Python) cocher "Show auto-import tooltip"
  * PyCharm vient d'ouvrir une fenêtre avec le contenu du "main.py" pour configurer les actions "UNDO" et "REDO"
  * Sélectionner tout le texte avec "CTRL-A" puis "CTRL-X" (Couper), puis "CTL-Z" (UNDO) et faites un REDO "CTRL-Y" et "PyCharm" va vous demander de choisir l'action du "CTRL-Y" raccourci pour faire un "REDO". (Dans 98% des éditeurs de texte, le "CTRL-Y" représente l'action "REDO"... pas chez JetBrains)

### Git
* Installer "GIT"
  * https://gitforwindows.org/
  * Le test de "GIT" se fait dans le programme "PyCharm"

### Pour finir : le clonage et le lancement!
  * Cloner ma dernière  version (lien plus bas)
  * Ouvrir "PyCharm". Cliquer sur le bouton à droite "GET FROM VCS"
      * Une fenêtre s'ouvre, copier le lien suivant dans le champ url : [**version by D4rkHeart**](https://github.com/D4rkHeart/Surdez_Leonardo_Info1D_AppRestaurant_164_V3TABLES)
      * Cliquer sur le bouton "CLONE"
      * Une fenêtre de sécurité "Trust and open project"... cliquer sur "Trust"
      * Laisser "PyCharm" créer un environnment virtuel, cliquer sur "Ok"
### Lancement
  * Lancer Uwamp
  * Lancer Pycharm
  * Ouvrez le projet 
  * lancer "run_mon_app"
  * Cliquer sur l'adresse : http://Votre.adresse.local:port
  * ET PROFITER DU CRUD DE QUALITE !

      

### Tips

#### Pour "rafraîchir" les versions des packages (Terminal de "PyCharm")
  * pip3 freeze > requirements.txt
  * pip3 install pipupgrade
  * pipupgrade --verbose --latest --yes


# LE PROJET
                        "Vivons de bonne soupe et non de beau langage"
## Description du projet

>L’idée de ce projet est de créer une interface qui communiquera avec une base de données qui permettra à des restaurateurs, des entreprises, des particuliers d’avoir une plateforme à disposition pour communiquer et accéder à des informations utiles sur un restaurant et des plats comme leur genre, la provenance de la cuisine, ou encore que contiennent les plats proposés. Le but ici est de rendre pratique pour l’utilisateur, la recherche d’un restaurant qui lui plaît et pour le restaurateur appâter des gens.

### Différente table :

* t_restaurants : Contient toutes les informations sur des restaurants
* t_plats : Contient toutes les informations sur des restaurants
* t_particularites :Contient toutes les informations sur les particularités potentiel d'un plat
* t_ingrédient : Contient toutes les informations sur les ingrédient potentiel d'un plat
* t_prix : Contient toutes les informations sur les prix potentiel des plats
* t_pays : Contient une liste de pays à attribuer
* t_plats_coûtent_prix : Table qui lie les prix aux plats
* t_plats_particularites : Table qui lie les particularites aux plats
* t_plats_contients_ingredients : Table qui lie les ingredients aux plats
### Feature :

>**Ajouter [Ajouter]:** Permet d'ajouter une ligne dans la table (Ex: un nouveau restaurant)  
>**Éditer [Edit]:** Permet d'éditer la ligne ou se trouve le bouton (Ex: changer le nom d'un restaurant)  
>**Effacer [Delete]:** Efface définitivement de la base de donnée l'élément sélectionner   
>**TAG [Table de liaison dans l'onglet "plat"]** : Permet de taguer un plat avec des éléments qui agrémenterons la précision du plat(Ex : ajouter des ingrédients au plat)