"""
    Fichier : gestion_prix_forms.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterPrix(FlaskForm):
    """
        Dans le formulaire "prix_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    prix_ajouter_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    type_prix_ajouter = StringField("Veuillez insérer un type ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(prix_ajouter_regexp,
                                                                           message="Pas de chiffres, de caractères "
                                                                                   "spéciaux, "
                                                                                   "d'espace à double, de double "
                                                                                   "apostrophe, de double trait union")
                                                                    ])
    valeur_prix_ajouter = StringField("Veuillez insérer un prix  ", validators=[Length(min=1, max=4, message="min 1 max 99.99")])
    submit = SubmitField("Enregistrer un restaurants")


class FormUpdatePrix(FlaskForm):
    """
        Dans le formulaire "prix_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    prix_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    type_prix_update = StringField("Veuillez modifier le type ",
                                         validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                     Regexp(prix_update_regexp,
                                                            message="Pas de chiffres, de "
                                                                    "caractères "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait "
                                                                    "union")
                                                     ])
    valeur_prix_update = StringField("Veuillez modifier le prix ",
                                    validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                Regexp(prix_update_regexp,
                                                       message="Pas de chiffres, de caractères "
                                                               "spéciaux, "
                                                               "d'espace à double, de double "
                                                               "apostrophe, de double trait union")
                                                ])
    date_prix_update = DateField("date de modification", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update restaurant")


class FormDeletePrix(FlaskForm):
    """
        Dans le formulaire "prix_delete.html"

        nom_prix_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    data_prix_delete = StringField("Effacer ce prix")
    submit_btn_del = SubmitField("Effacer ce prix")
    submit_btn_conf_del = SubmitField("Êtes-vous sur de vouloir l'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
