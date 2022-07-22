from peewee import *

from server import BaseModel

class Thesaurus(BaseModel):
    '''
    La classe Thesaurus permet d'accéder à toutes les données
    fixes de l'application.

        Attributs:
                | id (int): Id de la donnée
                | reference (int): référence de la donnée
                | label (str): label de la donnée
                | code (str): code de la donnée
    '''
    id = AutoField(primary_key=True)
    reference = TextField(default='')
    label = CharField(max_length=80)
    code = TextField(default='')

    class Meta:
        indexes = (
            (('code'), True)
        )