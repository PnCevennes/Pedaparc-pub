from peewee import *

from server import BaseModel
from models.animation.animation import Animation

class Commentaire(BaseModel):
    '''
    La classe Commentaire contient les données d'un commentaire lié
    à un objet Animation.

        Attributs:
                | id (int): Id du commentaire
                | date (date): date du commentaire
                | auteur (str): auteur du commentaire
                | commentaire (str): contenu du commentaire
    '''
    id = AutoField(primary_key=True)
    fk_id_anim = ForeignKeyField(Animation, backref='commentaires')
    date = DateField()
    auteur = CharField(max_length=100)
    commentaire = TextField()