from peewee import *

from server import BaseModel
from models.sequence.sequence import Sequence
from models.thesaurus.thesaurus import Thesaurus

SequenceThroughDeferred = DeferredThroughModel()
ThesaurusThroughDeffered = DeferredThroughModel()

class Mat_peda(BaseModel):
    '''
    La classe Mat_peda est la classe contenant les données pour les médias
    et outils facilitateurs.

        Attributs:
                | (media)(outil)  id (int): Id du media/outil
                | (media)(outil)  fk_type_mat (Thesaurus): type du média/outil
                | (media)(outil)  nom (str): nom du média/outil
                | (media)(outil)  description (str): description du média/outil
                | (media)(outil)  url (str): url de la ressource du média/outil
                | (media)         thematiques (Thesaurus[]): thematique(s) du média
                | (outil)         variante (str): variante de l'outil
                | (outil)         difficulte (str): difficulté de l'outil
                | (outil)         materiel (str): materiel de l'outil
                | (media)(outil)  date_modif (date): date de création du média/outil
                | (outil)         fk_type_mat_outil (Thesaurus): Type du média associé à l'outil
    '''
    id = AutoField()
    fk_type_mat = ForeignKeyField(Thesaurus)
    nom = CharField(max_length=100)
    description = TextField()
    url = CharField(max_length=250)
    localisation = CharField(max_length=50)
    sequence = ManyToManyField(Sequence, backref='materiel', through_model=SequenceThroughDeferred)
    thematiques = ManyToManyField(Thesaurus, through_model=ThesaurusThroughDeffered)
    variante = TextField()
    difficulte = ForeignKeyField(Thesaurus)
    materiel = TextField()
    date_modif = DateField(constraints=[SQL("DEFAULT (datetime('now'))")])
    fk_type_mat_outil = ForeignKeyField(Thesaurus, null=True, default=None)


class Rel_mat_peda_sequence(BaseModel):
    '''
    La classe Rel_mat_peda_thematique fait le lien entre
    l'objet Mat_peda et l'objet Sequence.

        Attributs:
                | fk_mat_peda (Mat_peda): objet Mat_peda
                | fk_sequence (Sequence): objet Sequence
    '''
    fk_mat_peda = ForeignKeyField(Mat_peda)
    fk_sequence = ForeignKeyField(Sequence)

    class Meta:
        indexes = (
            (('fk_mat_peda', 'fk_sequence'), True)
        )

SequenceThroughDeferred.set_model(Rel_mat_peda_sequence)

class Rel_mat_peda_thematique(BaseModel):
    '''
    La classe Rel_mat_peda_thematique fait le lien entre
    l'objet Mat_peda et l'objet Thesaurus.

        Attributs:
                | fk_mat_peda (Mat_peda): objet Mat_peda
                | fk_thes (Thesaurus): objet Thesaurus
    '''
    fk_mat_peda = ForeignKeyField(Mat_peda)
    fk_thes = ForeignKeyField(Thesaurus)

    class Meta:
        indexes = (
            (('fk_mat_peda', 'fk_thes'), True)
        )

ThesaurusThroughDeffered.set_model(Rel_mat_peda_thematique)