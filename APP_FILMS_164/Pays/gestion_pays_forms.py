"""
    Fichier : gestion_restaurants_forms.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterPays(FlaskForm):
    """
        Dans le formulaire "Pays_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_pays_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_pays_ajouter = StringField("Veuillez insérer un pays ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(nom_pays_regexp,
                                                                           message="Pas de chiffres, de caractères "
                                                                                   "spéciaux, "
                                                                                   "d'espace à double, de double "
                                                                                   "apostrophe, de double trait union")
                                                                    ])
    submit = SubmitField("Enregistrer un pays")


class FormUpdatePays(FlaskForm):
    """
        Dans le formulaire "pays_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_Pays_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_pays_update = StringField("Veuillez insérer votre modification ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_Pays_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_pays_update = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormDeletePays(FlaskForm):
    """
        Dans le formulaire "pays_delete.html"

        nom_pays_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_pays_delete = StringField("Effacer ce pays")
    submit_btn_del = SubmitField("Effacer ce pays")
    submit_btn_conf_del = SubmitField("Êtes-vous sur de vouloir l'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
