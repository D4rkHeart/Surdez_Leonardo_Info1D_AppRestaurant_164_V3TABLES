"""
    Fichier : gestion_ingredients_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterParticularites(FlaskForm):
    """
        Dans le formulaire "Particularites_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    particularites_ajouter_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_particularites = StringField("Veuillez insérer une particularité ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(particularites_ajouter_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer particularité")


class FormUpdateParticularites(FlaskForm):
    """
        Dans le formulaire "Particularite_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    particularite_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_particularites_update = StringField("Veuillez insérer ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(particularite_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_particularites_update = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update particularité")


class FormDeleteParticularites(FlaskForm):
    """
        Dans le formulaire "Particularite_delete_wtf.html"

        nom_Particularite_delete_wtf : Champ qui reçoit la valeur du particularité, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "particularité".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_particularité".
    """
    data_particularites = StringField("Effacer cette particularité")
    submit_btn_del = SubmitField("Effacer cette particularité")
    submit_btn_conf_del = SubmitField("Êtes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
