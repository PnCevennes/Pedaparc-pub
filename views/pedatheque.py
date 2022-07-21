import datetime
import json
import utils

import os
import os.path
import shutil
import re
import base64

from flask import (
        Blueprint,
        render_template,
        redirect,
        send_from_directory,
        request,
        g)

from werkzeug.utils import secure_filename

from models.animation import utils as animation
from models.sequence import utils as sequence
from models.thesaurus import utils as thesaurus
from models.commentaire import utils as commentaire

import config
from utils import auth, py3o_render

views = Blueprint('pedatheque',__name__)

#Cette fonction permet de créer un nouveau commentaire
@views.route('/create_comment/<id_anim>', methods=['POST'])
@auth.require_valid_user
def new_comment_form(id_anim):
    data = dict(request.form)
    data['user'] = g.user.name
    data['date'] = datetime.datetime.now().date()
    data['id_anim'] = id_anim
    commentaire.create_commentaire(data)

    return redirect('/pedatheque/'+id_anim)


#Cette fonction permet de supprimer un commentaire
@views.route('/delete_comment/<id_anim>/<id_commentaire>', methods=['GET'])
@auth.require_valid_user
def delete_comment(id_anim, id_commentaire):
    if g.user.is_admin or g.user.name==commentaire.get_commentaire(id_commentaire).auteur:
        commentaire.delete_commentaire(id_commentaire)
        return redirect('/pedatheque/'+id_anim)
    return redirect('/')


#Cette fonction permet d'afficher le form de recherche d'animations
@views.route('/', strict_slashes=False, methods=['GET'])
@auth.require_valid_user
def pedatheque_search_search_form():
    tags = {item: thesaurus.get_from_thes(code=item.code) for item 
        in utils.format('psearch', thesaurus.get_from_thes(idref=0))}
    return render_template('/tags_form.htm', tags=tags, action='pedatheque')


EN_COURS = 3
COMPLETE = 2
VALIDE = 1


#Cette fonction permet d'afficher les résultats de la recherche
@views.route('/results', methods=['GET'])
@auth.require_valid_user
def pedatheque_search_search_results():
    if request.args.get('auteur'):
        anims = [(item[0], item[0].tags[:], item[1])
            for item in animation.get_user_animations(request.args.get('auteur'))]
        return render_template('/pedatheque/search/results.htm', anims=anims)

    tags = []
    for item in utils.format('psearch', thesaurus.get_from_thes(idref=0)):
        tags = tags+request.args.getlist(item.nom)
    
    match = animation.match_anim_tags(tags)

    if not g.user.is_admin:
        match = [item for item in match if item[0].statut==VALIDE or item[0].auteurs==g.user.name]
    else:
        match = [item for item in match if not item[0].statut==EN_COURS]

    anims = [(item[0], item[0].tags[:], item[1]) for item in match]

    return render_template('/pedatheque/search/results.htm', anims=anims)


#Cette fonction permet d'afficher le display de l'animation consultée
@views.route('/<id_anim>', methods=['GET'])
@auth.require_valid_user
def pedatheque_search_anim_display(id_anim):
    return render_template('/pedatheque/search/anim_display.htm', 
        anim = animation.get_animation(id_anim), sequences=sequence.get_sequences(id_anim), 
        commentaires=commentaire.get_commentaires(id_anim), 
        tags=animation.get_animation(id_anim).tags[:])


#Cette fonction permet de supprimer l'animation concernée
@views.route('/<id_anim>/delete', methods=['GET'])
@auth.require_valid_user
def pedatheque_search_delete_anim(id_anim):
    anim = animation.get_animation(id_anim)
    if g.user.is_admin or (not anim.statut==1 and anim.auteurs==g.user.name):
        animation.delete_animation(id_anim)
        return redirect('/')
    return redirect('/')


#Cette fonction permet de mettre à jour le statut de l'animation concernée
@views.route('/<id_anim>/validate', methods=['GET'])
@auth.require_valid_user
def pedatheque_search_validate(id_anim):
    if g.user.is_admin:
        animation.validate(id_anim)
        return redirect('/pedatheque/'+id_anim)
    return redirect('/')


#Cette fonction permet de récupérer la liste des utilisateurs
@views.route('/get_users', methods=['GET'])
def pedatheque_search_author_autocomplete():
    chain = request.args['q']
    cnx = utils.auth.ldap_connect(config.LDAP_USER, config.LDAP_PASS)
    cnx.search(config.LDAP_BASE_PATH, '(sn=*)', attributes=['cn'])
    ldap_users = {'items': [{'title': str(item.cn)} for item 
        in cnx.entries if str(item.cn).casefold().startswith(chain.casefold())]}
    return json.dumps(ldap_users)


#Cette fonction permet de mettre à jour l'auteur de l'animation concernée
@views.route('/<id_anim>/update_author', methods=['POST'])
@auth.require_valid_user
@auth.require_admin_user
def pedatheque_search_update_author(id_anim):
    if g.user.is_admin:
        animation.update_author(id_anim, request.form['auteur'])
        return redirect('/pedatheque/'+id_anim)
    return redirect('/')


#Cette fonction permet de télécharger une animation
@views.route('/<id_anim>/download', methods=['GET'])
@auth.require_valid_user
def pedatheque_search_download_anim(id_anim):

    anim = animation.anim_delete_md(animation.get_animation(id_anim), 
        py3o_render.md_to_text)

    sequences = sequence.sequences_delete_md(sequence.get_sequences(id_anim), 
        py3o_render.md_to_text)

    medias_query = [item.materiel for item in sequence.get_sequences(id_anim)]
    media_list = []
    for medias in medias_query:
        for media in medias:
            media_list.append(media)

    tags = []
    for tag in animation.get_animation(id_anim).tags[:]:
        if tag.reference in [1,4,5]:
            with open('static/ressources/'+tag.nom+'.png', 'rb') as img_file:
                tags.append(base64.b64encode(img_file.read()))

    secure_name =  secure_filename(anim.titre)

    path = os.path.join(config.DOWNLOAD_FOLDER, secure_name)
    
    py3o_render.render_file(
        animation = anim, 
        sequences = sequences,
        medias = media_list,
        tags = tags,
        path=path)

    shutil.make_archive(path, 'zip', path)
    shutil.rmtree(path)
    
    return (send_from_directory(config.DOWNLOAD_FOLDER, 
        os.path.basename(secure_name+'.zip'), 
        as_attachment=True), 
        os.remove(path+'.zip'))