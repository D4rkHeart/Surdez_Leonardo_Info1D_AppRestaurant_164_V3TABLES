"""Gestion des "routes" FLASK et des données pour les prix.
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
from APP_FILMS_164.Prix.gestion_prix_forms import FormAjouterPrix
from APP_FILMS_164.Prix.gestion_prix_forms import FormDeletePrix
from APP_FILMS_164.Prix.gestion_prix_forms import FormUpdatePrix

"""
    Test : ex : http://127.0.0.1:5005/prix_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_prix_sel = 0 >> tous les prix.
                id_prix_sel = "n" affiche le prix dont l'id est "n"
"""


@app.route("/prix_afficher/<string:order_by>/<int:id_prix_sel>", methods=['GET', 'POST'])
def prix_afficher(order_by, id_prix_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_prix_sel == 0:
                    strsql_prix_afficher = """SELECT id_prix, prix_type, prix_valeur, updated_at FROM t_prix ORDER BY prix_type ASC"""
                    mc_afficher.execute(strsql_prix_afficher)
                elif order_by == "ASC":
                    valeur_id_prix_selected_dictionnaire = {"value_id_prix_selected": id_prix_sel}
                    strsql_prix_afficher = """SELECT * FROM t_prix WHERE id_prix = %(value_id_prix_selected)s"""
                    mc_afficher.execute(strsql_prix_afficher, valeur_id_prix_selected_dictionnaire)
                else:
                    strsql_prix_afficher = """SELECT id_prix, prix_type, prix_valeur, updated_at  FROM t_prix ORDER BY id_prix DESC"""
                    mc_afficher.execute(strsql_prix_afficher)
                data_prix = mc_afficher.fetchall()

                print("data_prix ", data_prix, " Type : ", type(data_prix))

                # Différencier les messages si la table est vide.
                if not data_prix and id_prix_sel == 0:
                    flash("""La table "t_prix" est vide. !!""", "warning")
                elif not data_prix and id_prix_sel > 0:
                    # Si l'utilisateur change l'id_prixs dans l'URL et que le prix n'existe pas,
                    flash(f"Le prix demandé n'existe pas !!", "warning")
                else:
                    # La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données sur les prix affichés !!", "success")

        except Exception as Exception_prix_afficher:
            raise Exception_prix_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{prix_afficher.__name__} ; "
                                          f"{Exception_prix_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Prix/Prix_afficher.html", data=data_prix)


"""
    Définition d'une "route" /prix_ajouter
    
    Test : ex : http://127.0.0.1:5005/prix_ajouter
    
    Paramètres : sans
    
    But : Ajouter un prix pour un film
    
    Remarque :  Dans le champ "name_prix_html" du formulaire "prix/Prix_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/prix_ajouter", methods=['GET', 'POST'])
def prix_ajouter():
    form = FormAjouterPrix()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                type_prix_ajouter = form.type_prix_ajouter.data
                valeur_prix_ajouter = form.valeur_prix_ajouter.data
                valeurs_insertion_dictionnaire = {"value_type": type_prix_ajouter, "value_valeur": valeur_prix_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_prix = """INSERT INTO t_prix (id_prix,prix_type,prix_valeur) VALUES (NULL,%(value_type)s,%(value_valeur)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_prix, valeurs_insertion_dictionnaire)
    
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('prix_afficher', order_by='DESC', id_prix_sel=0))

        except Exception as Exception_prix_ajouter:
            raise Exception_prix_ajouter(f"fichier : {Path(__file__).name};"
                                            f"{prix_ajouter.__name__};"
                                            f"{Exception_prix_ajouter}")

    return render_template("Prix/Prix_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /prix_update
    
    Test : ex cliquer sur le menu "prix" puis cliquer sur le bouton "EDIT" d'un "prix"
    
    Paramètres : sans
    
    But : Editer(update) un prix qui a été sélectionné dans le formulaire "Prix_afficher.html"
    
    Remarque :  Dans le champ "nom_prix_update" du formulaire "prix/prix_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/prix_update", methods=['GET', 'POST'])
def prix_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_prixs"
    id_prix_update = request.values['id_prix_btn_edit_html']
    # Objet formulaire pour l'UPDATE
    form_update = FormUpdatePrix()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "prix_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_prix_update = form_update.nom_prix_update.data
            type_prix_update = form_update.type_prix_update.data
            valeur_prix_update = form_update.valeur_prix_update.data
            date_prix_update = form_update.date_prix_update.data

            valeur_update_dictionnaire = {"value_id_prix": id_prix_update,
                                          "value_nom_prix": nom_prix_update,
                                          "value_type_prix": type_prix_update,
                                          "value_valeur_prix": valeur_prix_update,
                                          "value_date_prix_update": date_prix_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleprix = """UPDATE t_prix SET prix_type = %(value_name_prix)s, prix_valeur = %(value_type_prix)s, 
                updated_at = %(value_date_prix_update)s WHERE id_prix = %(value_id_prix)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleprix, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_prix_update"
            return redirect(url_for('prix_afficher', order_by="ASC", id_prix_sel=id_prix_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_prixs" et "nom" de la "t_prix"
            print(type(id_prix_update))
            str_sql_id_prix = "SELECT id_prix, prix_type, prix_valeur, updated_at FROM t_prix " \
                               "WHERE id_prix = %(value_id_prix)s"
            valeur_select_dictionnaire = {"value_id_prix": id_prix_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_prix, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom prix" pour l'UPDATE
            data_prix = mybd_conn.fetchone()

            # Afficher la valeur sélectionnée dans les champs du formulaire "prix_update.html"
            form_update.nom_prix_update.data = data_prix["prix_type"]
            form_update.type_prix_update.data = data_prix["prix_valeur"]
            form_update.date_prix_update.data = data_prix["updated_at"]
        print("No exception bro")
    except Exception as Exception_prix_update:
        print("exception bro")
        print(Exception_prix_update)
        raise Exception_prix_update(f"fichier : {Path(__file__).name}  ;  "
                                      f"{prix_update.__name__} ; "
                                      f"{Exception_prix_update}")

    return render_template("Prix/Prix_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /prix_delete
    
    Test : ex. cliquer sur le menu "prix" puis cliquer sur le bouton "DELETE" d'un "prix"
    
    Paramètres : sans
    
    But : Effacer(delete) un prix qui a été sélectionné dans le formulaire "Prix_afficher.html"
    
    Remarque :  Dans le champ "nom_prix_delete" du formulaire "prix/Prix_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/prix_delete", methods=['GET', 'POST'])
def prix_delete():
    data_prix_attribue_prix_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_prixs"
    id_prix_delete = request.values['id_prix_btn_delete_html']
    # Objet formulaire pour effacer le prix sélectionné.
    form_delete = FormDeletePrix()
    print("0.5")
    try:
        print(" on submit ", form_delete.validate_on_submit())
        print("0.7")
        if request.method == "POST" and form_delete.validate_on_submit():
            print("1")
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("prix_afficher", order_by="ASC", id_prix_sel=0))
            print("2")
            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Prix/Prix_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_prix_attribue_prix_delete = session['data_prix_attribue_prix_delete']
                print("data_prix_attribue_prix_delete ", data_prix_attribue_prix_delete)

                flash(f"Effacer le prix de façon défini  tive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer prix" qui va irrémédiablement EFFACER le prix
                btn_submit_del = True
            print("3")
            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_prix": id_prix_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)
                str_sql_delete_id_prixs = """DELETE FROM t_prix WHERE id_prix = %(value_id_prix)s"""
                # Ensuite on peut effacer le prix vu qu'il n'est plus "lié" (INNODB) dans la "t_prix_film"

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_prixs, valeur_delete_dictionnaire)

                flash(f"prix définitivement effacé !!", "success")
                print(f"prix définitivement effacé !!")

                # afficher les données
                return redirect(url_for('prix_afficher', order_by="ASC", id_prix_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_prix": id_prix_delete}
            with DBconnection() as mydb_conn:
                mydb_conn.execute(valeur_select_dictionnaire)
                data_prix_attribue_prix_delete = mydb_conn.fetchall()
                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "prix/Prix_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_prix_attribue_prix_delete'] = data_prix_attribue_prix_delete
                # Opération sur la BD pour récupérer "id_prixs" et "nom" de la "t_prix"
                str_sql_id_prix = "SELECT id_prix, prix_type, prix_valeur FROM t_prix WHERE id_prix = %(value_id_prix)s"
                mydb_conn.execute(str_sql_id_prix, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom prix" pour l'action DELETE
                data_prix_delete = mydb_conn.fetchone()
            # Afficher la valeur sélectionnée dans le champ du formulaire "Prix_delete.html"
            form_delete.type_prix_delete.data = data_prix_delete["prix_type"]
            form_delete.valeur_prix_delete.data = data_prix_delete["prix_valeur"]
            # Le bouton pour l'action "DELETE" dans le form. "Prix_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_prix_delete:
        raise Exception_prix_delete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{prix_delete.__name__} ; "
                                      f"{Exception_prix_delete}")

    return render_template("Prix/Prix_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_prix_attribue_prix_delete)
