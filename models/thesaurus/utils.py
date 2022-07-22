'''
Fichier contenant les fonctions utiles à la manipulation du thesaurus.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fonctions:

   | get_from_thes(idref=None) -> Thesaurus[]
   | create_thesaurus(data) -> Thesaurus
   | delete_thesaurus(id_thes)
   | get_thesaurus(id_thes) -> Thesaurus
   | get_pictos() -> Thesaurus[]
   | get_all_thes() -> Thesaurus[]
'''

from models.thesaurus.thesaurus import Thesaurus

#====================Thesaurus====================#

def get_from_thes(idref=None):
    '''
    Retourne les objets Thesaurus dont l'Id de référence ou le code de référence
    a été passé en paramètre.

        Param(s):
                | idref (int)(facultatif): Id de référence du type d'objets Thesaurus à renvoyer

        Return(s):
                | thes (Thesaurus[]): Liste de tous les objets Thesaurus correspondants au type d'objets passé en paramètre
    '''
    if idref is None: 
        raise ValueError('get_from_thes: idref doit être fourni')
    return Thesaurus.select().where(Thesaurus.reference==idref)[:]


def create_thesaurus(data):
    '''
    Crée un objet Thesaurus à partir des données passées en paramètre.

        Param(s):
                | data ({}): Dictionnaire contenant les attributs de l'objet

        Return(s):
                | thes (Thesaurus): Objet Thesaurus dont les attributs ont été remplis
    '''
    thes = Thesaurus.create(
        reference = data['reference'],
        label = data['label'])
    return thes


def delete_thesaurus(id_thes):
    '''
    Supprime l'objet Thesaurus dont l'id a été passé en paramètre.

        Param(s):
                | id_thes (int): Id de l'objet Thesaurus à supprimer
    '''
    Thesaurus.delete().where(Thesaurus.id==id_thes).execute()


def get_thesaurus(id_thes):
    '''
    Retourne l'objet Thesaurus dont l'Id a été passé en paramètre.

        Param(s):
                | id_thes (int): Id de l'objet Thesaurus à renvoyer

        Return(s):
                | thes (Thesaurus): Objet Thesaurus dont l'Id a été passé en paramètre
    '''
    return Thesaurus.get(id=id_thes)


def get_pictos():
    '''
    Retourne les objets Thesaurus associés à des pictogrammes.

        Return(s):
                | thes (Thesaurus[]): Liste de tous les objets Thesaurus associés à un pictogramme
    '''
    return Thesaurus.select().where(Thesaurus.reference.in_(['ref.thematiques','ref.lieux','ref.saison']))[:]


def get_all_thes():
    '''
    Retourne tous les objets Thesaurus qui ne sont pas des catégories.

        Return(s):
                | thes (Thesaurus[]): Liste de tous les objets Thesaurus qui ne sont pas des catégories
    '''
    return Thesaurus.select().where(Thesaurus.reference!='')[:]