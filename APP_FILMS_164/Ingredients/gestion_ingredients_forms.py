"""
    Fichier : gestion_ingredients_forms.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormAjouterIngredients(FlaskForm):
    """
        Dans le formulaire "Ingredients_ajouter.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    ingredients_ajouter_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_ingredients_ajouter = StringField("Veuillez insérer le nom de l'ingrédient (Ex: thon) ", validators=[Length(min=2, max=60, message="min 2 max 60")])
    type_ingredients_ajouter = StringField("Veuillez insérer son type (Ex: Féculents, volaile, etc) ", validators=[Length(min=2, max=25, message="min 2 max 20")])

    sucre_ingredients_ajouter = StringField("Le ingrédient est sucré ou salé ? ",
                                    validators=[Length(min=4, max=5, message="min 4, max 5"),
                                                Regexp(ingredients_ajouter_regexp,
                                                        message="Pas de chiffres, de caractères "
                                                                "spéciaux, "
                                                                "d'espace à double, de double "
                                                                "apostrophe, de double trait union")
                                                ])
    bio_ingredients_ajouter = StringField("Le ingrédient est bio ou non ? ",
                                    validators=[Length(min=3, max=3, message="oui ou non"),
                                                Regexp(ingredients_ajouter_regexp,
                                                        message="Pas de chiffres, de caractères "
                                                                "spéciaux, "
                                                                "d'espace à double, de double "
                                                                "apostrophe, de double trait union")
                                                ])
    pays_ingredients_ajouter = StringField("indiqué la provenance du pays avec son id (Ex: Suisse = 1) ", validators=[Length(min=1, max=2, message="min 2 max 20")])

    submit = SubmitField("Enregistrer un ingrédient")


class FormUpdateIngredients(FlaskForm):
    """
        Dans le formulaire "ingrédient_update.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ingredients_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_ingredients_update = StringField("Veuillez insérer le nom de l'ingrédient (Ex: thon) ",
                                         validators=[Length(min=2, max=60, message="min 2 max 60")])
    type_ingredients_update = StringField("Veuillez insérer son type (Ex: Féculents, volaile, etc) ",
                                          validators=[Length(min=2, max=25, message="min 2 max 20")])
    sucre_ingredients_update = StringField("Le ingrédient est sucré ou salé ? ",
                                           validators=[Length(min=4, max=5, message="min 4, max 5"),
                                                       Regexp(ingredients_update_regexp,
                                                              message="Pas de chiffres, de caractères "
                                                                      "spéciaux, "
                                                                      "d'espace à double, de double "
                                                                      "apostrophe, de double trait union")
                                                       ])
    bio_ingredients_update = StringField("Le ingrédient est bio ou non ? ",
                                         validators=[Length(min=3, max=3, message="oui ou non"),
                                                     Regexp(ingredients_update_regexp,
                                                            message="Pas de chiffres, de caractères "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait union")
                                                     ])
    pays_ingredients_update = StringField("indiqué la provenance du pays avec son id (Ex: Suisse = 1) ",
                                          validators=[Length(min=1, max=2, message="min 2 max 20")])
    date_ingredients_update = DateField("denière modification le: ", validators=[InputRequired("Date obligatoire"), DataRequired("Date non valide")])
    submit = SubmitField("Update ingredient")


class FormDeleteIngredients(FlaskForm):
    """
        Dans le formulaire "ingrédient_delete.html"

        nom_ingrédient_delete : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    data_ingredients = StringField("Effacer ce ingrédient")
    submit_btn_del = SubmitField("Effacer ce ingrédient")
    submit_btn_conf_del = SubmitField("Êtes-vous sur de vouloir l'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
