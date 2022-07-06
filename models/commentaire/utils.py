'''
Fichier contenant les fonctions utiles à la manipulation des commentaires.

Fonctions:

   create_commentaire(data) -> Commentaire
   get_commentaire(id_commentaire) -> Commentaire
   get_commentaires(id_anim) -> Commentaire
   delete_commentaire(id_com)
'''

from models.commentaire.commentaire import Commentaire
from models.animation.animation import Animation

#====================Commentaire====================#

def create_commentaire(data):
    '''
    Crée un objet Commentaire à partir des données passées en paramètre.

        Param(s):
                data ({}): Dictionnaire contenant les attributs de l'objet

        Return(s):
                commentaire (Commentaire): Objet Commentaire dont les attributs
                ont été remplis
    '''
    commentaire = Commentaire.create(
        fk_id_anim = Animation.get(id=data['id_anim']),
        date = data['date'],
        auteur = data['user'],
        commentaire = data['commentaire'])
    return commentaire


def get_commentaire(id_commentaire):
    '''
    Retourne l'objet Commentaire dont l'Id a été passé en paramètre.

        Param(s):
                id_commentaire (int): Id de l'objet Commentaire à retourner.

        Return(s):
                commentaire (Commentaire): Objet Commentaire dont l'Id a été 
                passé en paramètre
    '''
    return Commentaire.get(id=id_commentaire)


def get_commentaires(id_anim):
    '''
    Retourne tout les objets Commentaire liés à une animation dont l'Id est 
    passé en paramètre.

        Param(s):
                id_anim (str): Id de l'objet Animation dont les commentaires 
                sont voulus

        Return(s):
                commentaires (Commentaire[]): Liste de tout les objets 
                Commentaire liés à l'Animation dont l'Id est passé en paramètre
    '''
    return Animation.get(id=id_anim).commentaires


#Supprime le commentaire dont l'id est passé
def delete_commentaire(id_com):
    '''
    Supprime le commentaire dont l'Id est passé en paramètre.

        Param(s):
                id_com (int): Id de l'objet Commentaire à supprimer
    '''
    Commentaire.delete().where(Commentaire.id==id_com).execute()