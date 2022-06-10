"""Initialisation des variables d'environnement
    Auteur : OM 2021.03.03 Indispensable pour définir les variables indispensables dans tout le projet.
"""
import sys

from environs import Env
from flask import Flask
from flask import render_template

try:
    try:
        obj_env = Env()
        obj_env.read_env()
        HOST_MYSQL = obj_env("HOST_MYSQL")
        USER_MYSQL = obj_env("USER_MYSQL")
        PASS_MYSQL = obj_env("PASS_MYSQL")
        PORT_MYSQL = int(obj_env("PORT_MYSQL"))
        NAME_BD_MYSQL = obj_env("NAME_BD_MYSQL")
        NAME_FILE_DUMP_SQL_BD = obj_env("NAME_FILE_DUMP_SQL_BD")

        ADRESSE_SRV_FLASK = obj_env("ADRESSE_SRV_FLASK")
        DEBUG_FLASK = obj_env("DEBUG_FLASK")
        PORT_FLASK = obj_env("PORT_FLASK")
        SECRET_KEY_FLASK = obj_env("SECRET_KEY_FLASK")

        # OM 2022.04.11 Début de l'application
        app = Flask(__name__, template_folder="templates")
        print("app.url_map ____> ", app.url_map)

    except Exception as erreur:
        print(f"45677564530 init application variables d'environnement ou avec le fichier (son nom, son contenu)\n"
              f"{__name__}, "
              f"{erreur.args[0]}, "
              f"{repr(erreur)}, "
              f"{type(erreur)}")
        sys.exit()

    """
        Tout commence ici. Il faut "indiquer" les routes de l'applicationn.    
        Dans l'application les lignes ci-dessous doivent se trouver ici... soit après l'instanciation de la classe "Flask"
    """
    from APP_FILMS_164.database import database_tools
    from APP_FILMS_164.Pays import gestion_pays_crud
    from APP_FILMS_164.Restaurants import gestion_restaurants_crud
    from APP_FILMS_164.Plats import gestion_plats_crud
    from APP_FILMS_164.Ingredients import gestion_ingredients_crud
    from APP_FILMS_164.Particularites import gestion_particularites_crud
    from APP_FILMS_164.Prix import gestion_prix_crud
    from APP_FILMS_164.Plats_particularites import gestion_plats_particularites_crud

    from APP_FILMS_164.erreurs import msg_avertissements

    #Crée la route d'accès à la home page
    @app.route('/')
    @app.route('/homepage')
    def mapageprincipale():
        return render_template("home.html")

except Exception as Exception_init_app_films_164:
    print(f"4567756434 Une erreur est survenue {type(Exception_init_app_films_164)} dans"
          f"__init__ {Exception_init_app_films_164.args}")
    sys.exit()
