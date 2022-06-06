"""
    Fichier : gestion_ingredients_forms.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterPlats(FlaskForm):
    """
        Dans le formulaire "Ingredients_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    plats_ajouter_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_plats_ajouter = StringField("Veuillez insérer le nom du plat (Ex: Linguini sur sont lit de chocolat) ", validators=[Length(min=2, max=60, message="min 2 max 60")])
    type_plats_ajouter = StringField("Veuillez insérer son type (Ex: dessert) ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(plats_ajouter_regexp,
                                                                            message="Pas de chiffres, de caractères "
                                                                                    "spéciaux, "
                                                                                    "d'espace à double, de double "
                                                                                    "apostrophe, de double trait union")
                                                                    ])

    chaleur_plats_ajouter = StringField("est-ce que le plat est-il chaud ou froid ? ",
                                    validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                    Regexp(plats_ajouter_regexp,
                                                                           message="Pas de chiffres, de caractères "
                                                                                   "spéciaux, "
                                                                                   "d'espace à double, de double "
                                                                                   "apostrophe, de double trait union")
                                                                    ])

    submit = SubmitField("Enregistrer un plat")


class FormUpdatePlats(FlaskForm):
    """
        Dans le formulaire "plat_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    plats_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_plats_update = StringField("Veuillez insérer votre modification ", validators=[Length(min=2, max=60, message="min 2 max 60")])
    type_plats_update = StringField("Veuillez insérer votre modification ",
                                   validators=[Length(min=2, max=20, message="min 2 max 20"),
                                               Regexp(plats_update_regexp,
                                                      message="Pas de chiffres, de "
                                                              "caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait "
                                                              "union")
                                               ])

    chaleur_plats_update = StringField("Veuillez insérer votre modification ", validators=[Length(min=2, max=20, message="min 2 max 20")])

    date_plats_update = DateField("Essai date", validators=[InputRequired("Date obligatoire"),DataRequired("Date non valide")])

    submit = SubmitField("Update genre")


class FormDeletePlats(FlaskForm):
    """
        Dans le formulaire "plat_delete.html"

        nom_plat_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    data_plats = StringField("Effacer ce plat")
    submit_btn_del = SubmitField("Effacer ce plat")
    submit_btn_conf_del = SubmitField("Êtes-vous sur de vouloir l'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
