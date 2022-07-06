'''
Fichier contenant les fonctions utiles à la manipulation des sequences.

Fonctions:

   create_sequence(data,id_anim)
   update_sequence(data)
   get_sequence(id_seq) -> Sequence
   get_sequences(id_anim) -> Sequence[]
   first_sequences(id_anim,id_seq) -> Sequence[]
   last_sequences(id_anim,id_seq) -> Sequence[]
'''

from models.sequence.sequence import Sequence
from models.animation.animation import Animation, Rel_anim_sequence
from models.thesaurus.thesaurus import Thesaurus
from models.mat_peda.mat_peda import Rel_mat_peda_sequence, Mat_peda

#====================Sequence====================#

def create_or_update_all_sequences(id_anim, sequences):
    '''
    Crée ou met à jour les séquences d'un objet Animation
    à partir des données passées en paramètre.

        Param(s):
                id_anim (str): Id de l'objet Animation
                auquel les séquences seront liées
                sequences ([]): Liste contenant les
                données des séquences à créer ou mettre à jour
    '''
    for seq in sequences:
        if not seq.get('id',False):
            sequence = Sequence.create(
                titre = seq['titre'],
                description = seq['description'],
                fk_type_seq = Thesaurus.get(id=seq['fk_type_seq']),
                fk_duree = Thesaurus.get(id=seq['fk_duree']),
                fk_approche = Thesaurus.get(id=seq['fk_approche']),
                fk_modalite = Thesaurus.get(id=seq['fk_modalite']),
                objectifs = seq['objectifs'],
                materiel_div = seq['materiel_div'])

            Rel_anim_sequence.create(fk_anim = id_anim, fk_sequence = sequence.id)
        else:
            sequence = Sequence.get(id=seq['id'])
            sequence.titre = seq['titre']
            sequence.description = seq['description']
            sequence.fk_type_seq = Thesaurus.get(id=seq['fk_type_seq'])
            sequence.fk_duree = Thesaurus.get(id=seq['fk_duree'])
            sequence.fk_approche = Thesaurus.get(id=seq['fk_approche'])
            sequence.fk_modalite = Thesaurus.get(id=seq['fk_modalite'])
            sequence.objectifs = seq['objectifs']
            sequence.materiel_div = seq['materiel_div']
            sequence.save()

        Rel_mat_peda_sequence.delete().where(
            Rel_mat_peda_sequence.fk_sequence==sequence).execute()
        for media in seq['materiel']:
            rel_mat_peda_sequence = Rel_mat_peda_sequence.create(
                fk_mat_peda = Mat_peda.get(id=media), fk_sequence = sequence)


def get_sequence(id_seq):
    '''
    Retourne l'objet Sequence à partir de l'Id passé en paramètre.

        Param(s):
                id_seq (int): Id de l'objet Sequence a retourner

        Return(s):
                seq (Sequence): Objet Sequence dont l'id a été passé
                en paramètre
    '''
    return Sequence.get(id=id_seq)


def get_sequences(id_anim):
    '''
    Retourne tout les objets Sequence liés à l'objet Animation
    dont l'Id est passé en paramètre.

        Param(s):
                id_anim (str): Id de l'objet Animation dont les objets Sequence
                sont voulus

        Return(s):
                sequences (Sequence[]): Liste de tout les objets Sequence
                liés à l'objet Animation dont l'id a été passé en paramètre
    '''
    return Animation.get(id=id_anim).sequences[:]


def sequences_delete_md(sequences, md_to_text):
    '''
    Retourne une copie de la liste d'objets Sequence dont le markdown
    des attributs a été retiré.

        Param(s):
                sequences (Sequence[]): Liste d'objets Sequence dont le markdown
                doit être retiré des attributs
                md_to_text (function): Fonction permettant de transformer
                du markdown en plain text

        Return(s):
                copies (Sequence[]): Liste d'objets Sequence dont les attributs
                ne sont plus écrits en markdown
    '''
    copies = []

    for sequence in sequences:
    
        copie = Sequence()

        data = vars(sequence)['__data__']

        for item in data:
            if item == 'id':
                copie.id = sequences.index(sequence)
            elif not isinstance(data[item], int):
                setattr(copie, item, md_to_text(data[item]))
            else:
                setattr(copie, item, Thesaurus.get(id=data[item]))

        copies.append(copie)

    return copies