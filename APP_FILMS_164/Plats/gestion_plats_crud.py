"""Gestion des "routes" FLASK et des données pour les Plats.
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
from APP_FILMS_164.Plats.gestion_plats_forms import FormAjouterPlats
from APP_FILMS_164.Plats.gestion_plats_forms import FormDeletePlats
from APP_FILMS_164.Plats.gestion_plats_forms import FormUpdatePlats

"""
    Test : ex : http://127.0.0.1:5005/plats_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_plat_sel = 0 >> tous les Plats.
                id_plat_sel = "n" affiche le pays dont l'id est "n"
"""


@app.route("/plats_afficher/<string:order_by>/<int:id_plat_sel>", methods=['GET', 'POST'])
def plats_afficher(order_by, id_plat_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_plat_sel == 0:
                    strsql_plats_afficher = """SELECT id_plat, plat_nom, plat_type,plat_est_chaud, updated_at FROM t_plats ORDER BY plat_nom ASC"""
                    mc_afficher.execute(strsql_plats_afficher)
                elif order_by == "ASC":
                    valeur_id_plat_selected_dictionnaire = {"value_id_plat_selected": id_plat_sel}
                    strsql_plats_afficher = """SELECT * FROM t_plats WHERE id_plat = %(value_id_plat_selected)s"""
                    mc_afficher.execute(strsql_plats_afficher, valeur_id_plat_selected_dictionnaire)
                else:
                    strsql_plats_afficher = """SELECT id_plat, plat_nom, updated_at  FROM t_plats ORDER BY id_plat DESC"""
                    mc_afficher.execute(strsql_plats_afficher)
                data_plats = mc_afficher.fetchall()

                print("data_plats ", data_plats, " Type : ", type(data_plats))

                # Différencier les messages si la table est vide.
                if not data_plats and id_plat_sel == 0:
                    flash("""La table "t_plats" est vide. !!""", "warning")
                elif not data_plats and id_plat_sel > 0:
                    # Si l'utilisateur change l'id_plat dans l'URL et que le pays n'existe pas,
                    flash(f"Le plats demandé n'existe pas !!", "warning")
                else:
                    # La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données sur les plats affichés !!", "success")
                print(id_plat_sel)
        except Exception as Exception_plats_afficher:
            raise Exception_plats_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{plats_afficher.__name__} ; "
                                          f"{Exception_plats_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Plats/Plats_afficher.html", data=data_plats)


"""
    Définition d'une "route" /pays_ajouter
    
    Test : ex : http://127.0.0.1:5005/pays_ajouter
    
    Paramètres : sans
    
    But : Ajouter un pays pour un film
    
    Remarque :  Dans le champ "name_plats_html" du formulaire "Plats/Restaurants_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/plats_ajouter", methods=['GET', 'POST'])
def plats_ajouter():
    form = FormAjouterPlats()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_plats_ajouter = form.nom_plats_ajouter.data
                type_plats_ajouter = form.type_plats_ajouter.data
                chaleur_plats_ajouter = form.chaleur_plats_ajouter.data
                valeurs_insertion_dictionnaire = {"value_nom": nom_plats_ajouter, "value_type": type_plats_ajouter, "value_chaleur": chaleur_plats_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)
                strsql_insert_plats = """INSERT INTO t_plats (id_plat, plat_nom, plat_type, plat_est_chaud) VALUES (NULL,%(value_nom)s, %(value_type)s,%(value_chaleur)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_plats, valeurs_insertion_dictionnaire)
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('plats_afficher', order_by='DESC', id_plat_sel=0))

        except Exception as Exception_plats_ajouter:
            raise Exception_plats_ajouter(f"fichier : {Path(__file__).name};"
                                            f"{plats_ajouter.__name__};"
                                            f"{Exception_plats_ajouter}")
    return render_template("Plats/Plats_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /Plats_update
    
    Test : ex cliquer sur le menu "Plats" puis cliquer sur le bouton "EDIT" d'un "pays"
    
    Paramètres : sans
    
    But : Editer(update) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_plats_update" du formulaire "Plats/pays_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/plats_update", methods=['GET', 'POST'])
def plats_update():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_plat"
    id_plats_update = request.values['id_plat_btn_edit_html']
    # Objet formulaire pour l'UPDATE
    form_update = FormUpdatePlats()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "pays_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_plats_update = form_update.nom_plats_update.data
            type_plats_update = form_update.type_plats_update.data
            chaleur_plats_update = form_update.chaleur_plats_update.data
            date_plats_update = form_update.date_plats_update.data
            valeur_update_dictionnaire = {"value_id_plats": id_plats_update,
                                          "value_nom_plats": nom_plats_update,
                                          "value_type_plats": type_plats_update,
                                          "value_chaleur_plats": chaleur_plats_update,
                                          "value_date_plats": date_plats_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleplats = """UPDATE t_plats SET plat_nom = %(value_nom_plats)s, plat_type = %(value_type_plats)s, plat_est_chaud = %(value_chaleur_plats)s,
            updated_at = %(value_date_plats)s WHERE id_plat = %(value_id_plats)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleplats, valeur_update_dictionnaire)
            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_plats_update"
            return redirect(url_for('plats_afficher', order_by="ASC", id_plat_sel=id_plats_update))
            print("3")
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_plat" et "plat_nom" de la "t_plats"
            str_sql_id_plats = "SELECT id_plat, plat_nom, plat_type, plat_est_chaud, updated_at FROM t_plats " \
                               "WHERE id_plat = %(value_id_plats)s"
            valeur_select_dictionnaire = {"value_id_plats": id_plats_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_plats, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "plat_nom pays" pour l'UPDATE
            data_plats = mybd_conn.fetchone()
            print("data_plats ", data_plats, " type ", type(data_plats), " plats ",
                  data_plats["plat_nom"])
            # Afficher la valeur sélectionnée dans les champs du formulaire "pays_update.html"
            form_update.nom_plats_update.data = data_plats["plat_nom"]
            form_update.type_plats_update.data = data_plats["plat_type"]
            form_update.chaleur_plats_update.data = data_plats["plat_est_chaud"]
            form_update.date_plats_update.data = data_plats["updated_at"]
    except Exception as Exception_plats_update:
        raise Exception_plats_update(f"fichier : {Path(__file__).name}  ;  "
                                      f"{plats_update.__name__} ; "
                                      f"{Exception_plats_update}")
    return render_template("Plats/Plats_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /Plats_delete
    
    Test : ex. cliquer sur le menu "Plats" puis cliquer sur le bouton "DELETE" d'un "pays"
    
    Paramètres : sans
    
    But : Effacer(delete) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_plats_delete" du formulaire "Plats/Restaurants_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/plats_delete", methods=['GET', 'POST'])
def plats_delete():
    data_restaurant_attribue_Plats_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_plat"
    id_plats_delete = request.values['id_plat_btn_delete_html']

    # Objet formulaire pour effacer le pays sélectionné.
    form_delete = FormDeletePlats()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("plats_afficher", order_by="ASC", id_plat_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Plats/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_Plats_delete = session['data_restaurant_attribue_Plats_delete']
                print("data_restaurant_attribue_Plats_delete ", data_restaurant_attribue_Plats_delete)

                flash(f"Effacer le pays de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer pays" qui va irrémédiablement EFFACER le pays
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_plats": id_plats_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_id_plats = """DELETE FROM t_plats WHERE id_plat = %(value_id_plats)s"""
                # Manière brutale d'effacer d'abord la "fk_plats", même si elle n'existe pas dans la "t_plats_film"
                # Ensuite on peut effacer le pays vu qu'il n'est plus "lié" (INNODB) dans la "t_plats_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_plats, valeur_delete_dictionnaire)

                flash(f"plat définitivement effacé !!", "success")
                print(f"plat définitivement effacé !!")

                # afficher les données
                return redirect(url_for('plats_afficher', order_by="ASC", id_plat_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_plats": id_plats_delete}
            print(id_plats_delete, type(id_plats_delete))

            with DBconnection() as mydb_conn:
                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Plats/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_Plats_delete'] = data_restaurant_attribue_Plats_delete

                # Opération sur la BD pour récupérer "id_plat" et "plat_nom" de la "t_plats"
                str_sql_id_plats = "SELECT id_plat, plat_nom, plat_type, plat_est_chaud,updated_at FROM t_plats WHERE id_plat = %(value_id_plats)s"
                mydb_conn.execute(str_sql_id_plats, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                data_plats = mydb_conn.fetchone()
            # Afficher la valeur sélectionnée dans le champ du formulaire "Restaurants_delete.html"
            form_delete.nom_plats_delete.data = data_plats["plat_nom"]
            form_delete.type_plats_delete.data = data_plats["plat_type"]
            form_delete.chaleur_plats_delete.data = data_plats["plat_est_chaud"]
            form_delete.date_plats_delete.data = data_plats["updated_at"]


            # Le bouton pour l'action "DELETE" dans le form. "Restaurants_delete.html" est caché.
            btn_submit_del = False


    except Exception as Exception_plats_delete:
        raise Exception_plats_delete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{plats_delete.__name__} ; "
                                      f"{Exception_plats_delete}")

    return render_template("Plats/Plats_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_Plats_delete)
