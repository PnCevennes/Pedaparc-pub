'''
Fichier contenant les fonctions utiles à la manipulation des animations.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fonctions:

    | create_or_update_animation(data, tags) -> str
    | anim_to_dict(id_anim) -> dict
    | validate(id_anim)
    | update_author(id_anim, author)
    | get_animation(id_anim) ->  Animation
    | get_all_animations() ->  Animation[]
    | get_validated_animations() -> Animation[]
    | get_unvalidated_animations() ->  Animation[]
    | get_user_animations(user) ->  Animation[]
    | delete_animation(id_anim)
    | match_anim_tags(tags) ->  [Animation, pertinence][]
    | anim_delete_md(anim, md_to_text) ->  Animation
'''


from peewee import fn

import uuid

from models.animation.animation import Animation, Rel_anim_tag, Rel_anim_sequence
from models.sequence.sequence import Sequence
from models.mat_peda.mat_peda import Mat_peda, Rel_mat_peda_sequence
from models.thesaurus.thesaurus import Thesaurus
from models.commentaire.commentaire import Commentaire

#====================Animation====================#

def create_or_update_animation(data, tags):
    '''
    Crée ou met à jour un objet animation à partir des données
    passées en paramètre.

        Param(s):
                | data ({}): Dictionnaire contenant les attributs de l'objet
                | tags ({}): Dictionnaire contenant les mots-clés à associer

        Return(s):
                | id_anim (str): Id de l'objet Animation créé ou mis à jour

    '''
    if not data.get('id', False):
        anim_uuid = uuid.uuid4().hex
        animation = Animation.create(
            id = anim_uuid,
            titre = data['titre'],
            statut = data['statut'],
            auteurs = data['user'],
            pre_anim = data['pre_anim'],
            objectifs = data['objectifs'],
            lieu = data['lieu'],
            fk_duree = Thesaurus.get(id=data['fk_duree']),
            description = data['description'],
            public_specifique = data['public_specifique'],
            post_anim = data['post_anim'],
            date_modif = data['date_modif'])
    else:
        animation = Animation.get(id=data['id'])
        animation.titre = data['titre']
        animation.statut = 2
        animation.pre_anim = data['pre_anim']
        animation.objectifs = data['objectifs']
        animation.lieu = data['lieu']
        animation.fk_duree = Thesaurus.get(id=data['fk_duree'])
        animation.description = data['description']
        animation.public_specifique = data['public_specifique']
        animation.post_anim = data['post_anim']
        animation.date_modif = data['date_modif']
        animation.save()

    Rel_anim_tag.delete().where(Rel_anim_tag.fk_anim==animation).execute()
    Rel_anim_tag.create(fk_anim=animation, fk_thes=Thesaurus.get(id=data['fk_duree']))
    for tag in tags:
        try:
            Rel_anim_tag.create(fk_anim=animation, fk_thes=Thesaurus.get(id=tag))
        except Exception:
            pass

    return animation.id


def anim_to_dict(id_anim):
    '''
    Retourne un dictionnaire contenant les données d'un objet Animation.

        Param(s):
                | id_anim (str): Id de l'objet Animation dont on veut récupérer les attributs

        Return(s):
                | data ({}): Dictionnaire contenant tous les attributs de l'objet Animation dont l'id a été passé en paramètre

    '''
    anim = Animation.get(id=id_anim)

    data = vars(anim)['__data__']

    data['sequences'] = [vars(item)['__data__'] for item in anim.sequences[:]]

    for (seq_data, seq) in zip(data['sequences'], anim.sequences[:]):
        seq_data['materiel'] = [item.id for item in seq.materiel[:]]
    
    data['tags'] = [item.id for item in anim.tags[:]]
    
    return data


def validate(id_anim):
    '''
    Met le statut de l'animation à 1.

        Param(s):
                | id_anim (str): Id de l'objet Animation qui doit être validée

    '''
    anim = Animation.get(id=id_anim)
    anim.statut = 1
    anim.save()


def update_author(id_anim, author):
    '''
    Met à jour l'auteur de l'objet Animation.

        Param(s):
                | id_anim (str): Id de l'objet Animation dont l'auteur doit être modifié
                | author (str): Nom du nouvel auteur

    '''
    anim = Animation.get(id=id_anim)
    anim.auteurs = author
    anim.save()


def get_animation(id_anim):
    '''
    Retourne l'objet Animation dont l'Id a été passé en paramètre.

        Param(s):
                | id_anim (str): Id de l'objet Animation à retourner

        Return(s):
                | anim (Animation): Objet Animation dont l'Id a été passé en paramètre

    '''
    return Animation.get(id=id_anim)


def get_all_animations():
    '''
    Retourne tous les objets Animation.

        Return(s):
                | anims (Animation[]): Liste de tous les objets Animation

    '''
    return Animation.select()[:]


def get_validated_animations():
    '''
    Retourne tous les objets Animation dont le statut est à 1.

        Return(s):
                | anims (Animation[]): Liste de tous les objets Animation validés

    '''
    return Animation.select().where(Animation.statut==1)

def get_unvalidated_animations():
    '''
    Retourne tous les objets Animation dont le statut est à 2 ou 3.

        Return(s):
                | anims (Animation[]): Liste de tous les objets Animation non validés

    '''
    return Animation.select().where(Animation.statut.in_([2,3]))


#Retourne toutes les animations de l'user donné en paramètre
def get_user_animations(user):
    '''
    Retourne tous les objets Animation de l'auteur passé en paramètre.

        Param(s):
                | user (str): Nom de l'auteur des objets Animation voulus

        Return(s):
                | anims ([Animation, pertinence][]): Liste de tous les objets Animation dont l'auteur a été passé en paramètre

    '''
    return [[item, ''] for item in Animation.select().where(Animation.auteurs==user)]


def delete_animation(id_anim):
    '''
    Supprime l'objet Animation dont l'id a été passé en paramètre
    et toutes ses relations.

        Param(s):
                | id_anim (str): Id de l'objet Animation à supprimer

    '''
    #Suppression des relations thesaurus "tag"
    Rel_anim_tag.delete().where(Rel_anim_tag.fk_anim==id_anim).execute()
    #Suppression des séquences
    sequences = [item for item in Animation.get(id=id_anim).sequences]
    Rel_anim_sequence.delete().where(Rel_anim_sequence.fk_anim==id_anim).execute()
    Rel_mat_peda_sequence.delete().where(Rel_mat_peda_sequence.fk_sequence.in_(sequences)).execute()
    Sequence.delete().where(Sequence.id.in_(sequences)).execute()
    #Suppression des commentaires
    commentaires = [item for item in Animation.get(id=id_anim).commentaires]
    Commentaire.delete().where(Commentaire.id.in_(commentaires)).execute()
    #Suppression de l'animation
    Animation.delete().where(Animation.id==id_anim).execute()


def anim_sort(tab):
    return tab[1]


def anim_sort_alpha(tab):
    return tab[0].titre


def match_anim_tags(tags):
    '''
    Retourne tous les objets Animation et leur pertinence correspondants 
    aux mots-clés.

        Param(s):
                | tags (Thesaurus[]): Liste d'objets Thesaurus à utiliser pour la recherche

        Return(s):
                | anims ([Animation, pertinence][]): Liste de tous les objets Animation correspondant aux mots-clés données

    '''
    if tags:
        query = Rel_anim_tag.select(Rel_anim_tag.fk_anim, fn.COUNT(Rel_anim_tag.fk_anim)).where(
            Rel_anim_tag.fk_thes.in_(tags)
            ).group_by(Rel_anim_tag.fk_anim)
    else:
        query = Rel_anim_tag.select(Rel_anim_tag.fk_anim, fn.COUNT(Rel_anim_tag.fk_anim)).group_by(Rel_anim_tag.fk_anim)

    match = [[Animation.get(id=item['fk_anim']), (str(item['fk_anim_id'])+'/'+str(len(tags)) if len(tags) else '')] 
    for item in list(query.dicts())] 

    if not tags:
        return sorted(match, key=anim_sort_alpha, reverse=False)
    else:
        return sorted(match, key=anim_sort, reverse=True)


def anim_delete_md(anim, md_to_text):
    '''
    Retourne une copie de l'objet Animation dont le markdown
    des attributs a été retiré.

        Param(s):
                | anim (Animation): Objet Animation dont le markdown doit être retiré des attributs
                | md_to_text (function): Fonction permettant de transformer du markdown en plain text

        Return(s):
                | copie (Animation): Objet Animation dont les attributs ne sont plus écrits en markdown

    '''
    
    copie = Animation()

    data = vars(anim)['__data__']

    for item in data:
        if item == 'date_modif':
            pass
        elif not isinstance(data[item], int):
            setattr(copie, item, md_to_text(data[item]))
        else:
            setattr(copie, item, Thesaurus.get(id=data[item]))

    return copie