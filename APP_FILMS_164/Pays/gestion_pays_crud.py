"""Gestion des "routes" FLASK et des données pour les Pays.
Fichier : gestion_pays_crud.py
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
from APP_FILMS_164.Pays.gestion_pays_forms import FormWTFAjouterPays
from APP_FILMS_164.Pays.gestion_pays_forms import FormWTFDeletePays
from APP_FILMS_164.Pays.gestion_pays_forms import FormWTFUpdatePays

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /Pays_afficher
    
    Test : ex : http://127.0.0.1:5005/Pays_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_pays_sel = 0 >> tous les Pays.
                id_pays_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/Pays_afficher/<string:order_by>/<int:id_pays_sel>", methods=['GET', 'POST'])
def Pays_afficher(order_by, id_pays_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_pays_sel == 0:
                    strsql_pays_afficher = """SELECT id_pays, nom, updated_at FROM t_pays ORDER BY nom ASC"""
                    mc_afficher.execute(strsql_pays_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du pays sélectionné avec un nom de variable
                    valeur_id_pays_selected_dictionnaire = {"value_id_pays_selected": id_pays_sel}
                    strsql_pays_afficher = """SELECT * FROM t_pays WHERE id_pays = %(value_id_pays_selected)s"""

                    mc_afficher.execute(strsql_pays_afficher, valeur_id_pays_selected_dictionnaire)
                else:
                    strsql_pays_afficher = """SELECT id_pays, nom, updated_at  FROM t_pays ORDER BY id_pays DESC"""

                    mc_afficher.execute(strsql_pays_afficher)

                data_pays = mc_afficher.fetchall()

                print("data_pays ", data_pays, " Type : ", type(data_pays))

                # Différencier les messages si la table est vide.
                if not data_pays and id_pays_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_pays and id_pays_sel > 0:
                    # Si l'utilisateur change l'id_pays dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données Pays affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{Pays_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Pays/Pays_afficher.html", data=data_pays)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /Pays_ajouter
    
    Test : ex : http://127.0.0.1:5005/Pays_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "Pays/Pays_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Pays_ajouter", methods=['GET', 'POST'])
def Pays_ajouter_wtf():
    form = FormWTFAjouterPays()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_nom": name_genre}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_pays = """INSERT INTO t_pays (id_pays,nom) VALUES (NULL,%(value_nom)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_pays, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('Pays_afficher', order_by='DESC', id_pays_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("Pays/Pays_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /Pays_update
    
    Test : ex cliquer sur le menu "Pays" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "Pays_afficher.html"
    
    Remarque :  Dans le champ "nom_Pays_update_wtf" du formulaire "Pays/Pays_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Pays_update", methods=['GET', 'POST'])
def Pays_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_pays"
    id_Pays_update = request.values['id_pays_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePays()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "Pays_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_Pays_update = form_update.nom_Pays_update_wtf.data
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_pays": id_Pays_update,
                                          "value_name_pays": name_Pays_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_pays SET nom = %(value_name_pays)s, 
            updated_at = %(value_date_genre_essai)s WHERE id_pays = %(value_id_pays)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_Pays_update"
            return redirect(url_for('Pays_afficher', order_by="ASC", id_pays_sel=id_Pays_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_pays" et "nom" de la "t_genre"
            str_sql_id_pays = "SELECT id_pays, nom, updated_at FROM t_pays " \
                               "WHERE id_pays = %(value_id_pays)s"
            valeur_select_dictionnaire = {"value_id_pays": id_Pays_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_pays, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "Pays_update_wtf.html"
            form_update.nom_Pays_update_wtf.data = data_nom_genre["nom"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["updated_at"]

    except Exception as Exception_Pays_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{Pays_update_wtf.__name__} ; "
                                      f"{Exception_Pays_update_wtf}")

    return render_template("Pays/Pays_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /Pays_delete
    
    Test : ex. cliquer sur le menu "Pays" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "Pays_afficher.html"
    
    Remarque :  Dans le champ "nom_Pays_delete_wtf" du formulaire "Pays/Pays_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/Pays_delete", methods=['GET', 'POST'])
def Pays_delete_wtf():
    data_restaurant_attribue_Pays_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_pays"
    id_Pays_delete = request.values['id_pays_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletePays()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("Pays_afficher", order_by="ASC", id_pays_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Pays/Pays_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_Pays_delete = session['data_restaurant_attribue_Pays_delete']
                print("data_restaurant_attribue_Pays_delete ", data_restaurant_attribue_Pays_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_pays": id_Pays_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_genre_film WHERE fk_genre = %(value_id_pays)s"""
                str_sql_delete_idgenre = """DELETE FROM t_pays WHERE id_pays = %(value_id_pays)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('Pays_afficher', order_by="ASC", id_pays_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_pays": id_Pays_delete}
            print(id_Pays_delete, type(id_Pays_delete))
            

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_restaurant, restaurant_nom FROM t_restaurants 
                                            WHERE fk_pays = %(value_id_pays)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_restaurant_attribue_Pays_delete = mydb_conn.fetchall()
                print("##########")
                print("data_restaurant_attribue_Pays_delete...", data_restaurant_attribue_Pays_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Pays/Pays_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_Pays_delete'] = data_restaurant_attribue_Pays_delete

                # Opération sur la BD pour récupérer "id_pays" et "nom" de la "t_genre"
                str_sql_id_pays = "SELECT id_pays, nom FROM t_pays WHERE id_pays = %(value_id_pays)s"

                mydb_conn.execute(str_sql_id_pays, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "Pays_delete.html"
            form_delete.nom_Pays_delete_wtf.data = data_nom_genre["nom"]

            # Le bouton pour l'action "DELETE" dans le form. "Pays_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_Pays_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{Pays_delete_wtf.__name__} ; "
                                      f"{Exception_Pays_delete_wtf}")

    return render_template("Pays/Pays_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_restaurant_associes=data_restaurant_attribue_Pays_delete)
