import re

import markdown

import bleach

import config

def render_page(md_content):
    out = markdown.markdown(sanitize_text(md_content))
    out = re.sub('a href="http', 'a target="_blank" href="http', out)
    return out


def sanitize_text(text):
    return bleach.clean(text)


def format(formatage,tags):
    '''
    Retourne la liste de tous les objets Thesaurus
    correspondants au formatage donné.

        Param(s):
                formatage (str): Chaque formatage permet
                de renvoyer les objets thesaurus spécifiques à chaque situation
                    'psearch' -> ['ref.thematiques','ref.duree','ref.saison','ref.public','ref.lieux']
                    'msearch' -> ['ref.thematiques','ref.type_mat']
                tags (Thesaurus[]): Liste de tous les objets
                Thesaurus de référence

        Return(s):
                thes (Thesaurus): Liste de tous les objets Thesaurus correspondants au formatage
    '''
    if formatage=='psearch':
        return [item for item in tags if item.nom in config.tags_pedatheque_search]
    elif formatage=='msearch':
        return [item for item in tags if item.nom in config.tags_mediatheque_search]
    else:
        raiseError('mauvais format')

def user_format(username):
    return re.sub(' ', '+', username)