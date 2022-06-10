"""Gestion des "routes" FLASK et des données pour les restaurants.
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
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormAjouterRestaurants
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormDeleteRestaurants
from APP_FILMS_164.Restaurants.gestion_restaurants_forms import FormUpdateRestaurants

"""
    Test : ex : http://127.0.0.1:5005/restaurants_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_restaurant_sel = 0 >> tous les restaurants.
                id_restaurant_sel = "n" affiche le restaurants dont l'id est "n"
"""


@app.route("/restaurants_afficher/<string:order_by>/<int:id_restaurant_sel>", methods=['GET', 'POST'])
def restaurants_afficher(order_by, id_restaurant_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_restaurant_sel == 0:
                    strsql_restaurants_afficher = """SELECT id_restaurant, restaurant_nom, restaurant_type, updated_at FROM t_restaurants ORDER BY restaurant_nom ASC"""
                    mc_afficher.execute(strsql_restaurants_afficher)
                elif order_by == "ASC":
                    valeur_id_restaurant_selected_dictionnaire = {"value_id_restaurant_selected": id_restaurant_sel}
                    strsql_restaurants_afficher = """SELECT * FROM t_restaurants WHERE id_restaurant = %(value_id_restaurant_selected)s"""
                    mc_afficher.execute(strsql_restaurants_afficher, valeur_id_restaurant_selected_dictionnaire)
                else:
                    strsql_restaurants_afficher = """SELECT id_restaurant, restaurant_nom, restaurant_type, updated_at  FROM t_restaurants ORDER BY id_restaurant DESC"""
                    mc_afficher.execute(strsql_restaurants_afficher)
                data_restaurants = mc_afficher.fetchall()

                print("data_restaurants ", data_restaurants, " Type : ", type(data_restaurants))

                # Différencier les messages si la table est vide.
                if not data_restaurants and id_restaurant_sel == 0:
                    flash("""La table "t_restaurants" est vide. !!""", "warning")
                elif not data_restaurants and id_restaurant_sel > 0:
                    # Si l'utilisateur change l'id_restaurants dans l'URL et que le restaurants n'existe pas,
                    flash(f"Le restaurants demandé n'existe pas !!", "warning")
                else:
                    # La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données sur les restaurants affichés !!", "success")

        except Exception as Exception_restaurants_afficher:
            raise Exception_restaurants_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{restaurants_afficher.__name__} ; "
                                          f"{Exception_restaurants_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Restaurants/Restaurants_afficher.html", data=data_restaurants)


"""
    Définition d'une "route" /restaurants_ajouter
    
    Test : ex : http://127.0.0.1:5005/restaurants_ajouter
    
    Paramètres : sans
    
    But : Ajouter un restaurants pour un film
    
    Remarque :  Dans le champ "name_restaurants_html" du formulaire "restaurants/Restaurants_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/restaurants_ajouter", methods=['GET', 'POST'])
def restaurants_ajouter():
    form = FormAjouterRestaurants()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_restaurants_ajouter = form.nom_restaurants_ajouter.data
                type_restaurants_ajouter = form.type_restaurants_ajouter.data
                valeurs_insertion_dictionnaire = {"value_nom": name_restaurants_ajouter, "value_type": type_restaurants_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_restaurants = """INSERT INTO t_restaurants (id_restaurant,restaurant_nom,restaurant_type) VALUES (NULL,%(value_nom)s,%(value_type)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_restaurants, valeurs_insertion_dictionnaire)
    
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('restaurants_afficher', order_by='DESC', id_restaurant_sel=0))

        except Exception as Exception_restaurants_ajouter:
            raise Exception_restaurants_ajouter(f"fichier : {Path(__file__).name};"
                                            f"{restaurants_ajouter.__name__};"
                                            f"{Exception_restaurants_ajouter}")

    return render_template("Restaurants/Restaurants_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /restaurants_update
    
    Test : ex cliquer sur le menu "restaurants" puis cliquer sur le bouton "EDIT" d'un "restaurants"
    
    Paramètres : sans
    
    But : Editer(update) un restaurants qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_restaurants_update" du formulaire "restaurants/restaurants_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/restaurants_update", methods=['GET', 'POST'])
def restaurants_update():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_restaurants"
    id_restaurants_update = request.values['id_restaurants_btn_edit_html']
    # Objet formulaire pour l'UPDATE
    form_update = FormUpdateRestaurants()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "restaurants_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_restaurants_update = form_update.nom_restaurants_update.data
            type_restaurants_update = form_update.type_restaurants_update.data
            date_restaurants_update = form_update.date_restaurants_update.data

            valeur_update_dictionnaire = {"value_id_restaurants": id_restaurants_update,
                                          "value_name_restaurants": name_restaurants_update,
                                          "value_type_restaurants": type_restaurants_update,
                                          "value_date_restaurants_update": date_restaurants_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulerestaurants = """UPDATE t_restaurants SET restaurant_nom = %(value_name_restaurants)s, restaurant_type = %(value_type_restaurants)s, 
                updated_at = %(value_date_restaurants_update)s WHERE id_restaurant = %(value_id_restaurants)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulerestaurants, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_restaurants_update"
            return redirect(url_for('restaurants_afficher', order_by="ASC", id_restaurant_sel=id_restaurants_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_restaurants" et "nom" de la "t_restaurants"
            print(type(id_restaurants_update))
            str_sql_id_restaurants = "SELECT id_restaurant, restaurant_nom, restaurant_type, updated_at FROM t_restaurants " \
                               "WHERE id_restaurant = %(value_id_restaurants)s"
            valeur_select_dictionnaire = {"value_id_restaurants": id_restaurants_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_restaurants, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom restaurants" pour l'UPDATE
            data_restaurants = mybd_conn.fetchone()

            # Afficher la valeur sélectionnée dans les champs du formulaire "restaurants_update.html"
            form_update.nom_restaurants_update.data = data_restaurants["restaurant_nom"]
            form_update.type_restaurants_update.data = data_restaurants["restaurant_type"]
            form_update.date_restaurants_update.data = data_restaurants["updated_at"]
        print("No exception bro")
    except Exception as Exception_restaurants_update:
        print("exception bro")
        print(Exception_restaurants_update)
        raise Exception_restaurants_update(f"fichier : {Path(__file__).name}  ;  "
                                      f"{restaurants_update.__name__} ; "
                                      f"{Exception_restaurants_update}")

    return render_template("Restaurants/Restaurants_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /restaurants_delete
    
    Test : ex. cliquer sur le menu "restaurants" puis cliquer sur le bouton "DELETE" d'un "restaurants"
    
    Paramètres : sans
    
    But : Effacer(delete) un restaurants qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_restaurants_delete" du formulaire "restaurants/Restaurants_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/restaurants_delete", methods=['GET', 'POST'])
def restaurants_delete():
    data_restaurant_attribue_restaurants_delete = None
    print("-2")
    btn_submit_del = None
    print("-1")
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_restaurants"
    id_restaurants_delete = request.values['id_restaurants_btn_delete_html']
    print("0")
    # Objet formulaire pour effacer le restaurants sélectionné.
    form_delete = FormDeleteRestaurants()
    print("0.5")
    try:
        print(" on submit ", form_delete.validate_on_submit())
        print("0.7")
        print(request.method)
        if request.method == "POST" and form_delete.validate_on_submit():
            print("1")
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("restaurants_afficher", order_by="ASC", id_restaurant_sel=0))
            print("2")
            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Restaurants/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_restaurant_attribue_restaurants_delete = session['data_restaurant_attribue_restaurants_delete']
                print("data_restaurant_attribue_restaurants_delete ", data_restaurant_attribue_restaurants_delete)

                flash(f"Effacer le restaurants de façon défini  tive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer restaurants" qui va irrémédiablement EFFACER le restaurants
                btn_submit_del = True
            print("3")
            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_restaurants": id_restaurants_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)
                str_sql_delete_id_restaurants = """DELETE FROM t_restaurants WHERE id_restaurant = %(value_id_restaurants)s"""
                # Ensuite on peut effacer le restaurants vu qu'il n'est plus "lié" (INNODB) dans la "t_restaurants_film"

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_restaurants, valeur_delete_dictionnaire)

                flash(f"restaurants définitivement effacé !!", "success")
                print(f"restaurants définitivement effacé !!")

                # afficher les données
                return redirect(url_for('restaurants_afficher', order_by="ASC", id_restaurant_sel=0))

        if request.method == "GET":
            print("0.8")
            valeur_select_dictionnaire = {"value_id_restaurants": id_restaurants_delete}
            print(id_restaurants_delete, type(id_restaurants_delete))


            # Requête qui affiche tous les pays qui ont le restaurants que l'utilisateur veut effacer
            #str_sql_restaurants_pays_delete = """SELECT id_restaurant, restaurant_nom, restaurant_type FROM t_restaurants
            #                                WHERE FK_pays = %(value_id_restaurants)s"""
            #print(str_sql_restaurants_pays_delete)
            with DBconnection() as mydb_conn:
                #mydb_conn.execute(str_sql_restaurants_pays_delete, valeur_select_dictionnaire)
                #data_restaurant_attribue_restaurants_delete = mydb_conn.fetchall()
                #print("##########")
                #print("data_restaurant_attribue_restaurants_delete...", data_restaurant_attribue_restaurants_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "restaurants/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_restaurants_delete'] = data_restaurant_attribue_restaurants_delete
                print("5")
                # Opération sur la BD pour récupérer "id_restaurants" et "nom" de la "t_restaurants"
                str_sql_id_restaurants = """SELECT id_restaurant, restaurant_nom FROM t_restaurants WHERE id_restaurant = %(value_id_restaurants)s"""
                print(str_sql_id_restaurants)
                mydb_conn.execute(str_sql_id_restaurants, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom restaurants" pour l'action DELETE
                data_restaurants_delete = mydb_conn.fetchone()
            print(data_restaurants_delete)
            # Afficher la valeur sélectionnée dans le champ du formulaire "Restaurants_delete.html"
            form_delete.submit_info_restaurants_delete.data = data_restaurants_delete["restaurant_nom"]
            #form_delete.date_restaurants_delete.data = data_restaurants_delete["updated_at"]
            # Le bouton pour l'action "DELETE" dans le form. "Restaurants_delete.html" est caché.
            btn_submit_del = False

    except Exception as Exception_restaurants_delete:
        raise Exception_restaurants_delete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{restaurants_delete.__name__} ; "
                                      f"{Exception_restaurants_delete}")

    return render_template("restaurants/restaurants_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_restaurants_delete)
