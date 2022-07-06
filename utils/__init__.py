import re

import markdown

from bs4 import BeautifulSoup

import config

def render_page(md_content):
    out = markdown.markdown(md_content)
    out = re.sub('a href="http', 'a target="_blank" href="http', out)
    return out

def format(formatage,tags):
    '''
    Retourne la liste de tous les objets Thesaurus
    correspondants au formatage donné.

        Param(s):
                formatage (str): Chaque formatage permet
                de renvoyer les objets thesaurus spécifiques à chaque situation
                    'pcreate' -> ['ref.thematiques','ref.lieux','ref.saison','ref.public']
                    'psearch' -> ['ref.thematiques','ref.duree','ref.saison','ref.public','ref.lieux']
                    'msearch' -> ['ref.thematiques','ref.type_mat']
                    'screate' -> ['ref.approches','ref.modalites','ref.type_seq','ref.duree_seq']
                tags (Thesaurus[]): Liste de tout les objets
                Thesaurus de référence

        Return(s):
                thes (Thesaurus): Liste de tous les objets Thesaurus correspondants au formatage
    '''
    if formatage=='pcreate':
        return [item for item in tags if item.nom in config.tags_pedatheque_create]
    elif formatage=='psearch':
        return [item for item in tags if item.nom in config.tags_pedatheque_search]
    elif formatage=='msearch':
        return [item for item in tags if item.nom in config.tags_mediatheque_search]
    elif formatage=='screate':
        return [item for item in tags if item.nom in config.tags_sequence_create]
    else:
        raiseError('mauvais format')

def user_format(username):
    return re.sub(' ', '+', username)