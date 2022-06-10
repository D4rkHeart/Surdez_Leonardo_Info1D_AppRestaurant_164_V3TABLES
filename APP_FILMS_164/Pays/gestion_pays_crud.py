"""Gestion des "routes" FLASK et des données pour les Pays.
Fichier : gestion_prix_crud.py
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
from APP_FILMS_164.Pays.gestion_pays_forms import FormAjouterPays
from APP_FILMS_164.Pays.gestion_pays_forms import FormDeletePays
from APP_FILMS_164.Pays.gestion_pays_forms import FormUpdatePays

"""
    Test : ex : http://127.0.0.1:5005/pays_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_pays_sel = 0 >> tous les Pays.
                id_pays_sel = "n" affiche le pays dont l'id est "n"
"""


@app.route("/Pays_afficher/<string:order_by>/<int:id_pays_sel>", methods=['GET', 'POST'])
def pays_afficher(order_by, id_pays_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_pays_sel == 0:
                    strsql_pays_afficher = """SELECT id_pays, nom, updated_at FROM t_pays ORDER BY nom ASC"""
                    mc_afficher.execute(strsql_pays_afficher)
                elif order_by == "ASC":
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
                    flash("""La table "t_pays" est vide. !!""", "warning")
                elif not data_pays and id_pays_sel > 0:
                    # Si l'utilisateur change l'id_pays dans l'URL et que le pays n'existe pas,
                    flash(f"Le pays demandé n'existe pas !!", "warning")
                else:
                    # La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données sur les pays affichés !!", "success")

        except Exception as Exception_pays_afficher:
            raise Exception_pays_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{pays_afficher.__name__} ; "
                                          f"{Exception_pays_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Pays/pays_afficher.html", data=data_pays)


"""
    Définition d'une "route" /pays_ajouter
    
    Test : ex : http://127.0.0.1:5005/pays_ajouter
    
    Paramètres : sans
    
    But : Ajouter un pays pour un film
    
    Remarque :  Dans le champ "name_pays_html" du formulaire "Pays/Restaurants_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/pays_ajouter", methods=['GET', 'POST'])
def pays_ajouter():
    form = FormAjouterPays()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_pays_ajouter = form.nom_pays_ajouter.data
                valeurs_insertion_dictionnaire = {"value_nom": name_pays_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_pays = """INSERT INTO t_pays (id_pays,nom) VALUES (NULL,%(value_nom)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_pays, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('pays_afficher', order_by='DESC', id_pays_sel=0))

        except Exception as Exception_pays_ajouter:
            raise Exception_pays_ajouter(f"fichier : {Path(__file__).name};"
                                            f"{pays_ajouter.__name__};"
                                            f"{Exception_pays_ajouter}")

    return render_template("Pays/Pays_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /Pays_update
    
    Test : ex cliquer sur le menu "Pays" puis cliquer sur le bouton "EDIT" d'un "pays"
    
    Paramètres : sans
    
    But : Editer(update) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_pays_update" du formulaire "Pays/pays_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/Pays_update", methods=['GET', 'POST'])
def pays_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_pays"
    id_Pays_update = request.values['id_pays_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormUpdatePays()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "pays_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_Pays_update = form_update.nom_pays_update.data
            date_pays_essai = form_update.date_pays_update.data

            valeur_update_dictionnaire = {"value_id_pays": id_Pays_update,
                                          "value_name_pays": name_Pays_update,
                                          "value_date_pays_essai": date_pays_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulepays = """UPDATE t_pays SET nom = %(value_name_pays)s, 
            updated_at = %(value_date_pays_essai)s WHERE id_pays = %(value_id_pays)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulepays, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_Pays_update"
            return redirect(url_for('pays_afficher', order_by="ASC", id_pays_sel=id_Pays_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_pays" et "nom" de la "t_pays"
            str_sql_id_pays = "SELECT id_pays, nom, updated_at FROM t_pays " \
                               "WHERE id_pays = %(value_id_pays)s"
            valeur_select_dictionnaire = {"value_id_pays": id_Pays_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_pays, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom pays" pour l'UPDATE
            data_nom_pays = mybd_conn.fetchone()
            print("data_nom_pays ", data_nom_pays, " type ", type(data_nom_pays), " pays ",
                  data_nom_pays["nom"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "pays_update.html"
            form_update.nom_pays_update.data = data_nom_pays["nom"]
            form_update.date_pays_update.data = data_nom_pays["updated_at"]

    except Exception as Exception_pays_update:
        raise Exception_pays_update(f"fichier : {Path(__file__).name}  ;  "
                                      f"{pays_update.__name__} ; "
                                      f"{Exception_pays_update}")

    return render_template("Pays/Pays_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /Pays_delete
    
    Test : ex. cliquer sur le menu "Pays" puis cliquer sur le bouton "DELETE" d'un "pays"
    
    Paramètres : sans
    
    But : Effacer(delete) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_pays_delete" du formulaire "Pays/Restaurants_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/Pays_delete", methods=['GET', 'POST'])
def pays_delete():
    data_restaurant_attribue_Pays_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_pays"
    id_Pays_delete = request.values['id_pays_btn_delete_html']

    # Objet formulaire pour effacer le pays sélectionné.
    form_delete = FormDeletePays()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("pays_afficher", order_by="ASC", id_pays_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Pays/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_Pays_delete = session['data_restaurant_attribue_Pays_delete']
                print("data_restaurant_attribue_Pays_delete ", data_restaurant_attribue_Pays_delete)

                flash(f"Effacer le pays de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer pays" qui va irrémédiablement EFFACER le pays
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_pays": id_Pays_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_restaurants_pays = """ UPDATE t_restaurants SET FK_pays = null WHERE FK_pays = %(value_id_pays)s"""
                str_sql_delete_id_pays = """DELETE FROM t_pays WHERE id_pays = %(value_id_pays)s"""
                # Manière brutale d'effacer d'abord la "fk_pays", même si elle n'existe pas dans la "t_pays_film"
                # Ensuite on peut effacer le pays vu qu'il n'est plus "lié" (INNODB) dans la "t_pays_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_restaurants_pays, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_id_pays, valeur_delete_dictionnaire)

                flash(f"pays définitivement effacé !!", "success")
                print(f"pays définitivement effacé !!")

                # afficher les données
                return redirect(url_for('pays_afficher', order_by="ASC", id_pays_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_pays": id_Pays_delete}
            print(id_Pays_delete, type(id_Pays_delete))
            

            # Requête qui affiche tous les films_payss qui ont le pays que l'utilisateur veut effacer
            str_sql_pays_restaurants_delete = """SELECT id_restaurant, restaurant_nom FROM t_restaurants 
                                            WHERE FK_pays = %(value_id_pays)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_pays_restaurants_delete, valeur_select_dictionnaire)
                data_restaurant_attribue_Pays_delete = mydb_conn.fetchall()
                print("##########")
                print("data_restaurant_attribue_Pays_delete...", data_restaurant_attribue_Pays_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Pays/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_Pays_delete'] = data_restaurant_attribue_Pays_delete

                # Opération sur la BD pour récupérer "id_pays" et "nom" de la "t_pays"
                str_sql_id_pays = "SELECT id_pays, nom FROM t_pays WHERE id_pays = %(value_id_pays)s"

                mydb_conn.execute(str_sql_id_pays, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom pays" pour l'action DELETE
                data_nom_pays = mydb_conn.fetchone()
                print("data_nom_pays ", data_nom_pays, " type ", type(data_nom_pays), " pays ",
                      data_nom_pays["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "Restaurants_delete.html"
            form_delete.nom_pays_delete.data = data_nom_pays["nom"]

            # Le bouton pour l'action "DELETE" dans le form. "Restaurants_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_pays_delete:
        raise Exception_pays_delete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{pays_delete.__name__} ; "
                                      f"{Exception_pays_delete}")

    return render_template("Pays/Pays_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_Pays_delete)
