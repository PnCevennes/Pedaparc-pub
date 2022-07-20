from peewee import *

from server import BaseModel
from models.thesaurus.thesaurus import Thesaurus
from models.sequence.sequence import Sequence

SequenceThroughDeferred = DeferredThroughModel()
ThesaurusThroughDeffered = DeferredThroughModel()

class Animation(BaseModel):
    '''
    La classe Animation permet de contenir toutes les données
    d'une animation et est le composant central de l'application.

        Attributs:
                | id (str): Id de l'animation
                | titre (str): Titre de l'animation
                | statut (int): statut de l'animation (3=En cours, 2=Terminée, 1=Validée)
                | description (str): description de l'animation
                | auteurs (str): auteur de l'animation
                | pre_anim (str): avant l'animation
                | post_anim (str): après l'animation
                | objectifs (str): objectifs de l'animation
                | lieu (str): lieu de l'animation
                | public_specifique (str): public specifique de l'animation
                | date_modif (str): dernière date de modification de l'animation
                | fk_duree (Thesaurus): durée de l'animation
                | sequences (Sequence[]): sequences de l'animation
                | tags (Thesaurus[]): mots-clés de l'animation
    '''
    id = CharField(max_length=40, primary_key=True)
    titre = CharField(max_length=100)
    statut = IntegerField()
    description = TextField()
    auteurs = TextField()
    pre_anim = TextField()
    post_anim = TextField()
    objectifs = TextField()
    lieu = TextField()
    public_specifique = TextField()
    date_modif = DateField(constraints=[SQL("DEFAULT (datetime('now'))")])
    fk_duree = ForeignKeyField(Thesaurus)
    sequences = ManyToManyField(Sequence, through_model=SequenceThroughDeferred)
    tags = ManyToManyField(Thesaurus, through_model=ThesaurusThroughDeffered)

class Rel_anim_sequence(BaseModel):
    '''
    La classe Rel_anim_sequence permet de faire la liaison
    entre l'objet Animation et l'objet Sequence.

        Attributs:
                | fk_anim (Animation): objet Animation
                | fk_sequence (Sequence): objet Sequence
    '''
    fk_anim = ForeignKeyField(Animation)
    fk_sequence = ForeignKeyField(Sequence)

    class Meta:
        indexes = (
            (('fk_anim', 'fk_sequence'), True)
        )

SequenceThroughDeferred.set_model(Rel_anim_sequence)

class Rel_anim_tag(BaseModel):
    '''
    La classe Rel_anim_tag permet de faire la liaison
    entre l'objet Animation et l'objet Thesaurus.

        Attributs:
                | fk_anim (Animation): objet Animation
                | fk_thes (Thesaurus): objet Thesaurus
    '''
    fk_anim = ForeignKeyField(Animation)
    fk_thes = ForeignKeyField(Thesaurus)

    class Meta:
        indexes = (
            (('fk_anim', 'fk_thes'), True)
        )

ThesaurusThroughDeffered.set_model(Rel_anim_tag)