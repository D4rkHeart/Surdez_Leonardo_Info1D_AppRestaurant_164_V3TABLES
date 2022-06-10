"""
    Fichier : gestion_prix_forms.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterRestaurants(FlaskForm):
    """
        Dans le formulaire "restaurants_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    restaurants_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_restaurants_ajouter = StringField("Veuillez insérer un nom de restaurants ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(restaurants_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                    ])
    type_restaurants_ajouter = StringField("Veuillez insérer un type ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(restaurants_regexp,
                                                                           message="Pas de chiffres, de caractères "
                                                                                   "spéciaux, "
                                                                                   "d'espace à double, de double "
                                                                                   "apostrophe, de double trait union")
                                                                    ])
    submit = SubmitField("Enregistrer un restaurants")


class FormUpdateRestaurants(FlaskForm):
    """
        Dans le formulaire "restaurants_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    restaurants_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_restaurants_update = StringField("Veuillez modifier le nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(restaurants_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    type_restaurants_update = StringField("Veuillez modifier le type ",
                                         validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                     Regexp(restaurants_update_regexp,
                                                            message="Pas de chiffres, de "
                                                                    "caractères "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait "
                                                                    "union")
                                                     ])
    date_restaurants_update = DateField("date de modification", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update restaurant")


class FormDeleteRestaurants(FlaskForm):
    """
        Dans le formulaire "restaurants_delete.html"

        nom_restaurants_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    submit_info_restaurants_delete = StringField("Effacer ce restaurants")
    submit_btn_del = SubmitField("Effacer ce restaurants")
    submit_btn_conf_del = SubmitField("Êtes-vous sur de vouloir l'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
