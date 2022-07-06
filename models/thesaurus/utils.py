'''
Fichier contenant les fonctions utiles à la manipulation du thesaurus.

Fonctions:

   get_from_thes(idref=None, *, nom=None) -> Thesaurus[]
   create_thesaurus(data) -> Thesaurus
   get_thesaurus(id_thes) -> Thesaurus
'''

from models.thesaurus.thesaurus import Thesaurus

#====================Thesaurus====================#

def get_from_thes(idref=None, *, nom=None):
    '''
    Retourne les objets Thesaurus dont l'Id de référence ou le nom de référence
    a été passé en paramètre.

        Param(s):
                idref (int)(facultatif): Id de référence du type d'objets
                Thesaurus à renvoyer
                nom (str)(facultatif): nom de référence du type d'objets
                Thesaurus à renvoyer

        Return(s):
                thes (Thesaurus[]): Liste de tout les objets Thesaurus
                correspondants au type d'objets passé en paramètre
    '''
    if idref is None: 
        if nom:
            try:
                idref = Thesaurus.select().where(Thesaurus.nom == nom)[0].id
            except IndexError:
                return []
        else:
            raise ValueError('get_from_thes: idref ou nom doit être fourni')
    return Thesaurus.select().where(Thesaurus.reference==idref)[:]


def create_thesaurus(data):
    '''
    Crée un objet Thesaurus à partir des données passées en paramètre.

        Param(s):
                data ({}): Dictionnaire contenant les attributs de l'objet

        Return(s):
                thes (Thesaurus): Objet Thesaurus dont
                les attributs ont été remplis
    '''
    thes = Thesaurus.create(
        reference = data['reference'],
        nom = data['nom'])
    return thes


#Retourne l'objet thesaurus dont l'id est passé
def get_thesaurus(id_thes):
    '''
    Retourne l'objet Thesaurus dont l'Id a été passé en paramètre.

        Param(s):
                id_thes (int): Id de l'objet Thesaurus à renvoyer

        Return(s):
                thes (Thesaurus): Objet Thesaurus dont l'Id a été
                passé en paramètre
    '''
    return Thesaurus.get(id=id_thes)