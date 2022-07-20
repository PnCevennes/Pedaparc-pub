'''
Fichier contenant les fonctions utiles à la manipulation du thesaurus.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fonctions:

   | create_db()
   | pop_refs_thes()
   | pop_thes()
'''

import peewee

from server import db
from .thesaurus.thesaurus import Thesaurus
from .animation.animation import Animation, Rel_anim_sequence, Rel_anim_tag
from .sequence.sequence import Sequence
from .mat_peda.mat_peda import Mat_peda, Rel_mat_peda_sequence, Rel_mat_peda_thematique
from .commentaire.commentaire import Commentaire

def create_db():
    '''
    Crée les tables au niveau de la base de données.
    '''
    db.create_tables([
        Thesaurus,
        Animation,
        Sequence,
        Rel_anim_sequence,
        Mat_peda,
        Rel_mat_peda_sequence,
        Rel_mat_peda_thematique,
        Rel_anim_tag,
        Commentaire
        ])

def pop_refs_thes():
    """
    initialise le thésaurus
    attention, ne plus toucher une fois défini
    ne pas corriger les index
    si nouvelle reference, ajouter sur le tas

    id references:
        | 1 - thematiques 
        | 2 - type materiel
        | 3 - duree anim
        | 4 - lieu anim
        | 5 - saison anim
        | 6 - public anim
        | 7 - type sequence
        | 8 - duree sequence
        | 9 - approche sequence
        | 10 - modalites sequence
        | 76 - type outil
        | 84 - difficulte outil
    """
    for idx, nom, ref, label in [
            (1, 'ref.thematiques', 0, 'Thématiques'),
            (2, 'ref.type_mat', 0, 'Type'),
            (3, 'ref.duree', 0, 'Durée'),
            (4,'ref.lieux', 0, 'Lieux'), 
            (5, 'ref.saison', 0, 'Saison'), 
            (6, 'ref.public', 0, 'Public'),
            (7, 'ref.type_seq', 0, 'Type de séquence'),
            (8, 'ref.duree_seq', 0, 'Durée de séquence'),
            (9, 'ref.approches',0, 'Approches'),
            (10, 'ref.modalites',0, 'Modalités'),
            (76, 'ref.type_outil',0, 'Types d\'outil'),
            (84, 'ref.difficulte',0, 'Difficulté')]:
        try:
            Thesaurus.create(id=idx, nom=nom, reference=ref, label=label)
        except peewee.IntegrityError:
            print ('%s - %s déja existant' % (idx, nom))

def pop_thes():
    '''
    Entrées de base du thésaurus
    '''
    for idx, nom, ref, label in [
            (11, 'Agro-Pastoralisme', 1, ''),
            (12, 'Eau', 1, ''),
            (13, 'Faune', 1, ''),
            (14, 'Flore', 1, ''),
            (15, 'Forêt', 1, ''),
            (16, 'Insectes', 1, ''),
            (17, 'Oiseaux', 1, ''),
            (18, 'Nuit', 1, ''),
            (19, 'Patrimoine', 1, ''),
            (20, 'Handicap', 6, ''),
            (21, 'Journée', 3, ''),
            (22, 'Demi-journée', 3, ''),
            (23, 'Soirée', 3, ''),
            (24, 'Terrain', 4, ''),
            (25, 'Intérieur', 4, ''),
            (26, 'Printemps', 5, ''),
            (27, 'Été', 5, ''),
            (28, 'Automne', 5, ''),
            (29, 'Hiver', 5, ''),
            (30, 'Petite et Moyenne section', 6, ''),
            (31, 'Grande section - CP', 6, ''),
            (32, 'CE1 - CE2', 6, ''),
            (33, 'CM1 - CM2', 6, ''),
            (34, '6ème', 6, ''),
            (35, '5ème', 6, ''),
            (36, '4ème', 6, ''),
            (37, '3ème', 6, ''),
            (38, 'Lycée', 6, ''),
            (39, 'Grand public', 6, ''),
            (40, 'Classe unique', 6, ''),
            (41, 'Professionnels', 6, ''),
            (42, 'Introduction', 7, ''),
            (43, 'Développement', 7, ''),
            (44, 'Développement optionnel', 7, ''),
            (45, 'Conclusion', 7, ''),
            (46,'5 min',8, ''),
            (47,'10 min',8, ''),
            (48,'15 min',8, ''),
            (49,'20 min',8, ''),
            (50,'25 min',8, ''),
            (51,'30 min',8, ''),
            (52,'35 min',8, ''),
            (53,'40 min',8, ''),
            (54,'45 min',8, ''),
            (55,'50 min',8, ''),
            (56,'55 min',8, ''),
            (57,'1h',8, ''),
            (58,'1h30',8, ''),
            (59,'2h',8, ''),
            (60,'Artistique',9, ''),
            (61,'Scientifique',9, ''),
            (62,'Ludique',9, ''),
            (65,'Mise en pratique',9, ''),
            (67,'Sensible',9, ''),
            (68,'À l\'écoute',10, ''),
            (69,'En action',10, ''),
            (70,'Image',2, ''),
            (71,'Photo',2, ''),
            (72,'Vidéo',2, ''),
            (73,'Bande-son',2, ''),
            (74,'Support',2, ''),
            (75,'Contes',2, ''),
            (77,'Instaurer un cadre de confiance',76, 'instaureruncadre'),
            (78,'Débats',76, 'debats'),
            (79,'Émergence des représentations',76, 'emergencedesrespresentations'),
            (80,'Moments de calme',76, 'momentsdecalme'),
            (81,'En conclusion',76, 'enconclusion'),
            (82,'Jeux',76, 'jeux'),
            (83,'Multi-usage',76, 'multiusage'),
            (85,'Très facile',84,''),
            (86,'Facile',84,''),
            (87,'Moyen',84,''),
            (88,'Difficile',84,'')]:
        try:
            Thesaurus.create(id=idx, nom=nom, reference=ref, label=label)
        except peewee.IntegrityError:
            print ('%s - %s déja existant' % (idx, nom))
