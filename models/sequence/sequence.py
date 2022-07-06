from peewee import *

from server import BaseModel
from models.thesaurus.thesaurus import Thesaurus

class Sequence(BaseModel):
    '''
    Cette classe permet de créer une séquence liée à un objet Animation.

        Attributs:
                id (int): Id de la séquence
                titre (str): titre de la séquence
                objectifs (str): objectifs de la séquence
                fk_modalite (Thesaurus): modalité de la séquence
                fk_approche (Thesaurus): approche de la séquence
                description (str): description de la séquence
                materiel_div (str): matériel de la séquence
                fk_duree (Thesaurus): durée de la séquence
                fk_type_seq (Thesaurus): type de la séquence
    '''
    id = AutoField()
    titre = CharField(max_length=100)
    objectifs = TextField()
    fk_modalite = ForeignKeyField(Thesaurus)
    fk_approche = ForeignKeyField(Thesaurus)
    description = TextField()
    materiel_div = TextField()
    fk_duree = ForeignKeyField(Thesaurus)
    fk_type_seq = ForeignKeyField(Thesaurus)