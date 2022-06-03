"""Gestion des "routes" FLASK et des données pour les Particularites.
Fichier : gestion_plats_crud.py
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
from APP_FILMS_164.Particularites.gestion_particularites_forms import FormAjouterParticularite
from APP_FILMS_164.Particularites.gestion_particularites_forms import FormDeleteParticularite
from APP_FILMS_164.Particularites.gestion_particularites_forms import FormUpdateParticularite

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /Particularites_afficher
    
    Test : ex : http://127.0.0.1:5005/Particularites_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_particularite_sel = 0 >> tous les Particularites.
                id_particularite_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/Particularites_afficher/<string:order_by>/<int:id_particularite_sel>", methods=['GET', 'POST'])
def Particularites_afficher(order_by, id_particularite_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_particularite_sel == 0:
                    strsql_Particularites_afficher = """SELECT id_particularite, particularite_genre, updated_at FROM t_particularites ORDER BY particularite_genre ASC"""
                    mc_afficher.execute(strsql_Particularites_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du Particularites sélectionné avec un nom de variable
                    valeur_id_particularite_selected_dictionnaire = {"value_id_particularite_selected": id_particularite_sel}
                    strsql_Particularites_afficher = """SELECT * FROM t_particularites WHERE id_particularite = %(value_id_particularite_selected)s"""

                    mc_afficher.execute(strsql_Particularites_afficher, valeur_id_particularite_selected_dictionnaire)
                else:
                    strsql_Particularites_afficher = """SELECT id_particularite, particularite_genre, updated_at  FROM t_particularites ORDER BY id_particularite DESC"""

                    mc_afficher.execute(strsql_Particularites_afficher)

                data_Particularites = mc_afficher.fetchall()

                print("data_Particularites ", data_Particularites, " Type : ", type(data_Particularites))

                # Différencier les messages si la table est vide.
                if not data_Particularites and id_particularite_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_Particularites and id_particularite_sel > 0:
                    # Si l'utilisateur change l'id_particularite dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données Particularites affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{Particularites_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Particularites/Particularites_afficher.html", data=data_Particularites)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /Particularites_ajouter
    
    Test : ex : http://127.0.0.1:5005/Particularites_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "Particularites/Particularitess_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Particularites_ajouter", methods=['GET', 'POST'])
def Particularites_ajouter():
    form = FormWTFAjouterParticularites()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_nom": name_genre}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_particularites = """INSERT INTO t_particularites (id_particularite,particularite_genre) VALUES (NULL,%(value_nom)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_particularites, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('Particularites_afficher', order_by='DESC', id_particularite_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("Particularites/Particularites_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /Particularites_update
    
    Test : ex cliquer sur le menu "Particularites" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "Particularitess_afficher.html"
    
    Remarque :  Dans le champ "nom_Particularites_update_wtf" du formulaire "Particularites/Particularites_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Particularites_update", methods=['GET', 'POST'])
def Particularites_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_particularite"
    id_particularite_update = request.values['id_particularite_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateParticularites()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "Particularites_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_Particularites_update = form_update.nom_Particularites_update_wtf.data
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_particularite": id_particularite_update,
                                          "value_name_Particularites": name_Particularites_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_particularites SET nom = %(value_name_Particularites)s, 
            updated_at = %(value_date_genre_essai)s WHERE id_particularite = %(value_id_particularite)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_particularite_update"
            return redirect(url_for('Particularites_afficher', order_by="ASC", id_particularite_sel=id_particularite_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_particularite" et "nom" de la "t_genre"
            str_sql_id_particularite = "SELECT id_particularite, nom, updated_at FROM t_particularites " \
                               "WHERE id_particularite = %(value_id_particularite)s"
            valeur_select_dictionnaire = {"value_id_particularite": id_particularite_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_particularite, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "Particularites_update_wtf.html"
            form_update.nom_Particularites_update_wtf.data = data_nom_genre["nom"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["updated_at"]

    except Exception as Exception_Particularites_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{Particularites_update_wtf.__name__} ; "
                                      f"{Exception_Particularites_update_wtf}")

    return render_template("Particularites/Particularites_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /Particularites_delete
    
    Test : ex. cliquer sur le menu "Particularites" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "Particularitess_afficher.html"
    
    Remarque :  Dans le champ "nom_Particularites_delete_wtf" du formulaire "Particularites/Particularitess_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/Particularites_delete", methods=['GET', 'POST'])
def Particularites_delete_wtf():
    data_restaurant_attribue_Particularites_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_particularite"
    id_particularite_delete = request.values['id_particularite_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteParticularites()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("Particularites_afficher", order_by="ASC", id_particularite_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Particularites/Particularitess_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_Particularites_delete = session['data_restaurant_attribue_Particularites_delete']
                print("data_restaurant_attribue_Particularites_delete ", data_restaurant_attribue_Particularites_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_particularite": id_particularite_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """ UPDATE t_restaurants SET FK_Particularites = null WHERE FK_Particularites = %(value_id_particularite)s"""
                str_sql_delete_idgenre = """DELETE FROM t_particularites WHERE id_particularite = %(value_id_particularite)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('Particularites_afficher', order_by="ASC", id_particularite_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_particularite": id_particularite_delete}
            print(id_particularite_delete, type(id_particularite_delete))
            

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_restaurant, restaurant_nom FROM t_restaurants 
                                            WHERE FK_Particularites = %(value_id_particularite)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_restaurant_attribue_Particularites_delete = mydb_conn.fetchall()
                print("##########")
                print("data_restaurant_attribue_Particularites_delete...", data_restaurant_attribue_Particularites_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Particularites/Particularitess_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_Particularites_delete'] = data_restaurant_attribue_Particularites_delete

                # Opération sur la BD pour récupérer "id_particularite" et "nom" de la "t_genre"
                str_sql_id_particularite = "SELECT id_particularite, nom FROM t_particularites WHERE id_particularite = %(value_id_particularite)s"

                mydb_conn.execute(str_sql_id_particularite, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "Particularitess_delete.html"
            form_delete.nom_Particularites_delete_wtf.data = data_nom_genre["nom"]

            # Le bouton pour l'action "DELETE" dans le form. "Particularitess_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_Particularites_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{Particularites_delete_wtf.__name__} ; "
                                      f"{Exception_Particularites_delete_wtf}")

    return render_template("Particularites/Particularites_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_Particularites_delete)
