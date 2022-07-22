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
        | 'ref.thematiques' - thematiques 
        | 'ref.type_mat' - type materiel
        | 'ref.duree' - duree anim
        | 'ref.lieux' - lieu anim
        | 'ref.saison' - saison anim
        | 'ref.public' - public anim
        | 'ref.type_seq' - type sequence
        | 'ref.duree_seq' - duree sequence
        | 'ref.approches' - approche sequence
        | 'ref.modalites' - modalites sequence
        | 'ref.type_outil' - type outil
        | 'ref.difficulte' - difficulte outil
    """
    for idx, label, ref, code in [
            (1, 'Thématiques', '', 'ref.thematiques'),
            (2, 'Type', '', 'ref.type_mat'),
            (3, 'Durée', '', 'ref.duree'),
            (4,'Lieux', '', 'ref.lieux'), 
            (5, 'Saison', '', 'ref.saison'), 
            (6, 'Public', '', 'ref.public'),
            (7, 'Type de séquence', '', 'ref.type_seq'),
            (8, 'Durée de séquence', '', 'ref.duree_seq'),
            (9, 'Approches', '', 'ref.approches'),
            (10, 'Modalités', '', 'ref.modalites'),
            (76, 'Types d\'outils', '', 'ref.type_outil'),
            (84, 'Difficulté', '', 'ref.difficulte')]:
        try:
            Thesaurus.create(id=idx, label=label, reference=ref, code=code)
        except peewee.IntegrityError:
            print ('%s - %s déja existant' % (idx, label))

def pop_thes():
    '''
    Entrées de base du thésaurus
    '''
    for idx, label, ref, code in [
            (11, 'Agro-Pastoralisme', 'ref.thematiques', ''),
            (12, 'Eau', 'ref.thematiques', ''),
            (13, 'Faune', 'ref.thematiques', ''),
            (14, 'Flore', 'ref.thematiques', ''),
            (15, 'Forêt', 'ref.thematiques', ''),
            (16, 'Insectes', 'ref.thematiques', ''),
            (17, 'Oiseaux', 'ref.thematiques', ''),
            (18, 'Nuit', 'ref.thematiques', ''),
            (19, 'Patrimoine', 'ref.thematiques', ''),
            (20, 'Handicap', 'ref.public', ''),
            (21, 'Journée', 'ref.duree', ''),
            (22, 'Demi-journée', 'ref.duree', ''),
            (23, 'Soirée', 'ref.duree', ''),
            (24, 'Terrain', 'ref.lieux', ''),
            (25, 'Intérieur', 'ref.lieux', ''),
            (26, 'Printemps', 'ref.saison', ''),
            (27, 'Été', 'ref.saison', ''),
            (28, 'Automne', 'ref.saison', ''),
            (29, 'Hiver', 'ref.saison', ''),
            (30, 'Petite et Moyenne section', 'ref.public', ''),
            (31, 'Grande section - CP', 'ref.public', ''),
            (32, 'CE1 - CE2', 'ref.public', ''),
            (33, 'CM1 - CM2', 'ref.public', ''),
            (34, '6ème', 'ref.public', ''),
            (35, '5ème', 'ref.public', ''),
            (36, '4ème', 'ref.public', ''),
            (37, '3ème', 'ref.public', ''),
            (38, 'Lycée', 'ref.public', ''),
            (39, 'Grand public', 'ref.public', ''),
            (40, 'Classe unique', 'ref.public', ''),
            (41, 'Professionnels', 'ref.public', ''),
            (42, 'Introduction', 'ref.type_seq', 'intro'),
            (43, 'Développement', 'ref.type_seq', 'dvp'),
            (44, 'Développement optionnel', 'ref.type_seq', 'dvpopt'),
            (45, 'Conclusion', 'ref.type_seq', 'conclu'),
            (46,'5 min', 'ref.duree_seq', ''),
            (47,'10 min', 'ref.duree_seq', ''),
            (48,'15 min', 'ref.duree_seq', ''),
            (49,'20 min', 'ref.duree_seq', ''),
            (50,'25 min', 'ref.duree_seq', ''),
            (51,'30 min', 'ref.duree_seq', ''),
            (52,'35 min', 'ref.duree_seq', ''),
            (53,'40 min', 'ref.duree_seq', ''),
            (54,'45 min', 'ref.duree_seq', ''),
            (55,'50 min', 'ref.duree_seq', ''),
            (56,'55 min', 'ref.duree_seq', ''),
            (57,'1h', 'ref.duree_seq', ''),
            (58,'1h30', 'ref.duree_seq', ''),
            (59,'2h', 'ref.duree_seq', ''),
            (60,'Artistique', 'ref.approches', ''),
            (61,'Scientifique', 'ref.approches', ''),
            (62,'Ludique', 'ref.approches', ''),
            (65,'Mise en pratique', 'ref.approches', ''),
            (67,'Sensible', 'ref.approches', ''),
            (68,'À l\'écoute', 'ref.modalites', ''),
            (69,'En action', 'ref.modalites', ''),
            (70,'Image', 'ref.type_mat', 'image'),
            (71,'Photo', 'ref.type_mat', 'photo'),
            (72,'Vidéo', 'ref.type_mat', 'video'),
            (73,'Bande-son', 'ref.type_mat', 'bandeson'),
            (74,'Support', 'ref.type_mat', 'support'),
            (75,'Conte', 'ref.type_mat', 'contes'),
            (77,'Instaurer un cadre de confiance', 'ref.type_outil', 'instaureruncadre'),
            (78,'Débats', 'ref.type_outil', 'debats'),
            (79,'Émergence des représentations', 'ref.type_outil', 'emergencedesrespresentations'),
            (80,'Moments de calme', 'ref.type_outil', 'momentsdecalme'),
            (81,'En conclusion', 'ref.type_outil', 'enconclusion'),
            (82,'Jeux', 'ref.type_outil', 'jeux'),
            (83,'Multi-usage', 'ref.type_outil', 'multiusage'),
            (85,'Très facile', 'ref.difficulte', ''),
            (86,'Facile', 'ref.difficulte', ''),
            (87,'Moyen', 'ref.difficulte', ''),
            (88,'Difficile', 'ref.difficulte', '')]:
        try:
            Thesaurus.create(id=idx, label=label, reference=ref, code=code)
        except peewee.IntegrityError:
            print ('%s - %s déja existant' % (idx, label))
