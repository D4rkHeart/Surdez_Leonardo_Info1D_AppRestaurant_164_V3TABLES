"""Gestion des "routes" FLASK et des données pour les Plats.
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
from APP_FILMS_164.Ingredients.gestion_ingredients_forms import FormAjouterIngredients
from APP_FILMS_164.Ingredients.gestion_ingredients_forms import FormDeleteIngredients
from APP_FILMS_164.Ingredients.gestion_ingredients_forms import FormUpdateIngredients

"""
    Test : ex : http://127.0.0.1:5005/ingredients_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_ingredient_sel = 0 >> tous les Plats.
                id_ingredient_sel = "n" affiche le pays dont l'id est "n"
"""


@app.route("/ingredients_afficher/<string:order_by>/<int:id_ingredient_sel>", methods=['GET', 'POST'])
def ingredients_afficher(order_by, id_ingredient_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_ingredient_sel == 0:
                    strsql_ingredients_afficher = """SELECT id_ingredient, ingredient_nom, ingredient_est_sucre,provenance_est_bio,categorie_type,FK_pays, updated_at FROM t_ingredients ORDER BY ingredient_nom ASC"""
                    mc_afficher.execute(strsql_ingredients_afficher)
                elif order_by == "ASC":
                    valeur_id_ingredient_selected_dictionnaire = {"value_id_ingredient_selected": id_ingredient_sel}
                    strsql_ingredients_afficher = """SELECT * FROM t_ingredients WHERE id_ingredient = %(value_id_ingredient_selected)s"""
                    mc_afficher.execute(strsql_ingredients_afficher, valeur_id_ingredient_selected_dictionnaire)
                else:
                    strsql_ingredients_afficher = """SELECT id_ingredient, ingredient_nom, ingredient_est_sucre,provenance_est_bio,categorie_type,FK_pays, updated_at  FROM t_ingredients ORDER BY id_ingredient DESC"""
                    mc_afficher.execute(strsql_ingredients_afficher)
                data_ingredients = mc_afficher.fetchall()
                # Différencier les messages si la table est vide.
                if not data_ingredients and id_ingredient_sel == 0:
                    flash("""La table "t_ingredients" est vide. !!""", "warning")
                elif not data_ingredients and id_ingredient_sel > 0:
                    # Si l'utilisateur change l'id_ingredient dans l'URL et que le pays n'existe pas,
                    flash(f"L'ingredients demandé n'existe pas !!", "warning")
                else:
                    # La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données sur les ingredients affichés !!", "success")
                print(id_ingredient_sel)
        except Exception as Exception_ingredients_afficher:
            raise Exception_ingredients_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{ingredients_afficher.__name__} ; "
                                          f"{Exception_ingredients_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("Ingredients/Ingredients_afficher.html", data=data_ingredients)


"""
    Définition d'une "route" /pays_ajouter
    
    Test : ex : http://127.0.0.1:5005/pays_ajouter
    
    Paramètres : sans
    
    But : Ajouter un pays pour un film
    
    Remarque :  Dans le champ "name_ingredients_html" du formulaire "Ingredients/Restaurants_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/ingredients_ajouter", methods=['GET', 'POST'])
def ingredients_ajouter():
    form = FormAjouterIngredients()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_ingredients_ajouter = form.nom_ingredients_ajouter.data
                type_ingredients_ajouter = form.type_ingredients_ajouter.data
                sucre_ingredients_ajouter = form.sucre_ingredients_ajouter.data
                bio_ingredients_ajouter = form.bio_ingredients_ajouter.data
                pays_ingredients_ajouter = form.pays_ingredients_ajouter.data
                valeurs_insertion_dictionnaire = {"value_nom": nom_ingredients_ajouter, "value_type": type_ingredients_ajouter, "value_sucre": sucre_ingredients_ajouter, "value_bio": bio_ingredients_ajouter, "value_pays": pays_ingredients_ajouter}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)
                print("1")
                strsql_insert_ingredients = """INSERT INTO t_ingredients (id_ingredient, ingredient_nom, ingredient_est_sucre,provenance_est_bio,categorie_type,FK_pays) VALUES (NULL,%(value_nom)s, %(value_sucre)s, %(value_bio)s, %(value_type)s, %(value_pays)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_ingredients, valeurs_insertion_dictionnaire)
                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('ingredients_afficher', order_by='DESC', id_ingredient_sel=0))

        except Exception as Exception_ingredients_ajouter:
            raise Exception_ingredients_ajouter(f"fichier : {Path(__file__).name};"
                                            f"{ingredients_ajouter.__name__};"
                                            f"{Exception_ingredients_ajouter}")
    return render_template("Ingredients/Ingredients_ajouter.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /Ingredients_update
    
    Test : ex cliquer sur le menu "Plats" puis cliquer sur le bouton "EDIT" d'un "pays"
    
    Paramètres : sans
    
    But : Editer(update) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_ingredients_update" du formulaire "Ingredients/pays_update.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/ingredients_update", methods=['GET', 'POST'])
def ingredients_update():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_ingredient"
    id_ingredients_update = request.values['l']
    # Objet formulaire pour l'UPDATE
    form_update = FormUpdateIngredients()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "pays_update.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_ingredients_update = form_update.nom_ingredients_update.data
            type_ingredients_update = form_update.type_ingredients_update.data
            sucre_ingredients_update = form_update.sucre_ingredients_update.data
            bio_ingredients_update = form_update.bio_ingredients_update.data
            pays_ingredients_update = form_update.pays_ingredients_update.data
            date_ingredients_update = form_update.date_ingredients_update.data


            valeur_update_dictionnaire = {"value_id_ingredients": id_ingredients_update,
                                          "value_nom_ingredients": nom_ingredients_update,
                                          "value_type_ingredients": type_ingredients_update,
                                          "value_sucre_ingredients": sucre_ingredients_update,
                                          "value_bio_ingredients": bio_ingredients_update,
                                          "value_pays_ingredients": pays_ingredients_update,
                                          "value_date_ingredients": date_ingredients_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleingredients = """UPDATE t_ingredients SET ingredient_nom = %(value_nom_ingredients)s, ingredient_est_sucre = %(value_sucre_ingredients)s, provenance_est_bio = %(value_bio_ingredients)s, categorie_type = %(value_type_ingredients)s, FK_pays = %(value_pays_ingredients)s,
            updated_at = %(value_date_ingredients)s WHERE id_ingredient = %(value_id_ingredients)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleingredients, valeur_update_dictionnaire)
            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_ingredients_update"
            return redirect(url_for('ingredients_afficher', order_by="ASC", id_ingredient_sel=id_ingredients_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_ingredient" et "ingredient_nom" de la "t_ingredients"
            str_sql_id_ingredients = "SELECT id_ingredient, ingredient_nom, ingredient_est_sucre, provenance_est_bio, categorie_type, FK_pays, updated_at FROM t_ingredients " \
                               "WHERE id_ingredient = %(value_id_ingredients)s"
            valeur_select_dictionnaire = {"value_id_ingredients": id_ingredients_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_ingredients, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "ingredient_nom pays" pour l'UPDATE
            data_ingredients = mybd_conn.fetchone()
            # Afficher la valeur sélectionnée dans les champs du formulaire "pays_update.html"
            form_update.nom_ingredients_update.data = data_ingredients["ingredient_nom"]
            form_update.sucre_ingredients_update.data = data_ingredients["ingredient_est_sucre"]
            form_update.bio_ingredients_update.data = data_ingredients["provenance_est_bio"]
            form_update.type_ingredients_update.data = data_ingredients["categorie_type"]
            form_update.pays_ingredients_update.data = data_ingredients["FK_pays"]
            form_update.date_ingredients_update.data = data_ingredients["updated_at"]
    except Exception as Exception_ingredients_update:
        raise Exception_ingredients_update(f"fichier : {Path(__file__).name}  ;  "
                                      f"{ingredients_update.__name__} ; "
                                      f"{Exception_ingredients_update}")
    return render_template("Ingredients/Ingredients_update.html", form_update=form_update)



"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /Ingredients_delete
    
    Test : ex. cliquer sur le menu "Plats" puis cliquer sur le bouton "DELETE" d'un "pays"
    
    Paramètres : sans
    
    But : Effacer(delete) un pays qui a été sélectionné dans le formulaire "Restaurants_afficher.html"
    
    Remarque :  Dans le champ "nom_ingredients_delete" du formulaire "Ingredients/Restaurants_delete.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/ingredients_delete", methods=['GET', 'POST'])
def ingredients_delete():
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_ingredient"
    id_ingredients_delete = request.values['id_ingredient_btn_delete_html']

    # Objet formulaire pour effacer le pays sélectionné.
    form_delete = FormDeleteIngredients()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("ingredients_afficher", order_by="ASC", id_ingredient_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "Ingredients/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                flash(f"Effacer le pays de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer pays" qui va irrémédiablement EFFACER le pays
                btn_submit_del = True
                print("2")

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_ingredients": id_ingredients_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_id_ingredients = """DELETE FROM t_ingredients WHERE id_ingredient = %(value_id_ingredients)s"""
                # Manière brutale d'effacer d'abord la "fk_ingredients", même si elle n'existe pas dans la "t_ingredients_film"
                # Ensuite on peut effacer le pays vu qu'il n'est plus "lié" (INNODB) dans la "t_ingredients_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_ingredients, valeur_delete_dictionnaire)

                flash(f"plat définitivement effacé !!", "success")
                print(f"plat définitivement effacé !!")

                # afficher les données
                return redirect(url_for('ingredients_afficher', order_by="ASC", id_ingredient_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_ingredients": id_ingredients_delete}
            print(id_ingredients_delete, type(id_ingredients_delete))

            with DBconnection() as mydb_conn:
                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "Ingredients/Restaurants_delete.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_restaurant_attribue_Ingredients_delete'] = data_restaurant_attribue_Ingredients_delete

                # Opération sur la BD pour récupérer "id_ingredient" et "ingredient_nom" de la "t_ingredients"
                str_sql_id_ingredients = "SELECT id_ingredient, ingredient_nom, ingredient_est_sucre, provenance_est_bio,updated_at FROM t_ingredients WHERE id_ingredient = %(value_id_ingredients)s"
                mydb_conn.execute(str_sql_id_ingredients, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                data_ingredients = mydb_conn.fetchone()
            # Afficher la valeur sélectionnée dans le champ du formulaire "Restaurants_delete.html"
            form_delete.nom_ingredients_delete.data = data_ingredients["ingredient_nom"]
            form_delete.type_ingredients_delete.data = data_ingredients["ingredient_est_sucre"]
            form_delete.chaleur_ingredients_delete.data = data_ingredients["provenance_est_bio"]
            form_delete.date_ingredients_delete.data = data_ingredients["updated_at"]


            # Le bouton pour l'action "DELETE" dans le form. "Restaurants_delete.html" est caché.
            btn_submit_del = False


    except Exception as Exception_ingredients_delete:
        raise Exception_ingredients_delete(f"fichier : {Path(__file__).name}  ;  "
                                      f"{ingredients_delete.__name__} ; "
                                      f"{Exception_ingredients_delete}")

    return render_template("Ingredients/Ingredients_delete.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,   
                           data_restaurant_associes=data_restaurant_attribue_Ingredients_delete)
