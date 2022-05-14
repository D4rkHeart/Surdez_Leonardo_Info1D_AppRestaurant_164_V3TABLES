"""Gestion des "routes" FLASK et des données pour les restaurants.
Fichier : gestion_restaurants_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormAjouterRestaurants
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormDeleteRestaurants
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormUpdateRestaurants

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /Restaurants_afficher
    
    Test : ex : http://127.0.0.1:5005/Restaurants_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_restaurant_sel = 0 >> tous les restaurants.
                id_restaurant_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/Restaurants_afficher/<string:order_by>/<int:id_restaurant_sel>", methods=['GET', 'POST'])
def Restaurants_afficher(order_by, id_restaurant_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_restaurant_sel == 0:
                    strsql_Restaurants_afficher = """SELECT id_restaurant, restaurant_nom, restaurant_type, updated_at FROM t_restaurants ORDER BY restaurant_nom ASC"""
                    mc_afficher.execute(strsql_Restaurants_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du restaurants sélectionné avec un nom de variable
                    valeur_id_restaurant_selected_dictionnaire = {"value_id_restaurant_selected": id_restaurant_sel}
                    strsql_Restaurants_afficher = """SELECT * FROM t_restaurants WHERE id_restaurant = %(value_id_restaurant_selected)s"""

                    mc_afficher.execute(strsql_Restaurants_afficher, valeur_id_restaurant_selected_dictionnaire)
                else:
                    strsql_Restaurants_afficher = """SELECT id_restaurant, restaurant_nom, restaurant_type, updated_at  FROM t_restaurants ORDER BY id_restaurant DESC"""

                    mc_afficher.execute(strsql_Restaurants_afficher)

                data_restaurants = mc_afficher.fetchall()

                print("data_restaurants ", data_restaurants, " Type : ", type(data_restaurants))

                # Différencier les messages si la table est vide.
                if not data_restaurants and id_restaurant_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_restaurants and id_restaurant_sel > 0:
                    # Si l'utilisateur change l'id_restaurant dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données restaurants affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{Restaurants_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Restaurant/Restaurants_afficher.html", data=data_restaurants)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /restaurants_ajouter
    
    Test : ex : http://127.0.0.1:5005/Restaurants_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "restaurants/restaurants_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Restaurants_ajouter", methods=['GET', 'POST'])
def Restaurants_ajouter():
    form = FormWTFAjouterrestaurants()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_nom": name_genre}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_restaurants = """INSERT INTO t_restaurants (id_restaurant,restaurant_nom) VALUES (NULL,%(value_nom)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_restaurants, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('Restaurants_afficher', order_by='DESC', id_restaurant_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("restaurants/restaurants_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /restaurants_update
    
    Test : ex cliquer sur le menu "restaurants" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_restaurants_update_wtf" du formulaire "restaurants/restaurants_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Restaurants_update", methods=['GET', 'POST'])
def Restaurants_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_restaurant"
    id_restaurant_update = request.values['id_restaurant_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdaterestaurants()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "restaurants_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_restaurants_update = form_update.nom_restaurants_update_wtf.data
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_restaurant": id_restaurant_update,
                                          "value_name_restaurants": name_restaurants_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_restaurants SET restaurant_nom = %(value_name_restaurants)s, 
            updated_at = %(value_date_genre_essai)s WHERE id_restaurant = %(value_id_restaurant)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_restaurant_update"
            return redirect(url_for('Restaurants_afficher', order_by="ASC", id_restaurant_sel=id_restaurant_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_restaurant" et "nom" de la "t_genre"
            str_sql_id_restaurant = "SELECT id_restaurant, nom, updated_at FROM t_restaurants " \
                               "WHERE id_restaurant = %(value_id_restaurant)s"
            valeur_select_dictionnaire = {"value_id_restaurant": id_restaurant_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_restaurant, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "restaurants_update_wtf.html"
            form_update.nom_restaurants_update_wtf.data = data_nom_genre["nom"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["updated_at"]

    except Exception as Exception_restaurants_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{restaurants_update_wtf.__name__} ; "
                                      f"{Exception_restaurants_update_wtf}")

    return render_template("restaurants/restaurants_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /restaurants_delete
    
    Test : ex. cliquer sur le menu "restaurants" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_restaurants_delete_wtf" du formulaire "restaurants/restaurants_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/Restaurants_delete", methods=['GET', 'POST'])
def Restaurants_delete_wtf():
    data_restaurant_attribue_restaurants_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_restaurant"
    id_restaurant_delete = request.values['id_restaurant_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleterestaurants()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("Restaurants_afficher", order_by="ASC", id_restaurant_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "restaurants/restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_restaurants_delete = session['data_restaurant_attribue_restaurants_delete']
                print("data_restaurant_attribue_restaurants_delete ", data_restaurant_attribue_restaurants_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_restaurant": id_restaurant_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """ UPDATE t_restaurants SET FK_restaurants = null WHERE FK_restaurants = %(value_id_restaurant)s"""
                str_sql_delete_idgenre = """DELETE FROM t_restaurants WHERE id_restaurant = %(value_id_restaurant)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('Restaurants_afficher', order_by="ASC", id_restaurant_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_restaurant": id_restaurant_delete}
            print(id_restaurant_delete, type(id_restaurant_delete))
            

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_restaurant, restaurant_nom FROM t_restaurants 
                                            WHERE FK_restaurants = %(value_id_restaurant)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_restaurant_attribue_restaurants_delete = mydb_conn.fetchall()
                print("##########")
                print("data_restaurant_attribue_restaurants_delete...", data_restaurant_attribue_restaurants_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "restaurants/restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_restaurants_delete'] = data_restaurant_attribue_restaurants_delete

                # Opération sur la BD pour récupérer "id_restaurant" et "nom" de la "t_genre"
                str_sql_id_restaurant = "SELECT id_restaurant, nom FROM t_restaurants WHERE id_restaurant = %(value_id_restaurant)s"

                mydb_conn.execute(str_sql_id_restaurant, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "restaurants_delete.html"
            form_delete.nom_restaurants_delete_wtf.data = data_nom_genre["nom"]

            # Le bouton pour l'action "DELETE" dans le form. "restaurants_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_restaurants_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{restaurants_delete_wtf.__name__} ; "
                                      f"{Exception_restaurants_delete_wtf}")

    return render_template("Restaurants/Restaurants_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_restaurants_delete)
