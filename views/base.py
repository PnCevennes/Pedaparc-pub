import datetime
from datetime import date, timedelta

import json

from flask import (
        Blueprint,
        render_template,
        current_app,
        redirect,
        url_for,
        request,
        g)
from itsdangerous import TimedSerializer

import config
from utils import auth

from models.animation import utils as animation
from models.mat_peda import utils as mat_peda
from models.thesaurus import utils as thesaurus

import os
import os.path
import shutil

import utils
from utils.mail import send_mail

views = Blueprint('main', __name__)

#Cette fonction permet d'afficher la page d'accueil.
@views.route('/')
@auth.require_valid_user
def index():
    if g.user.is_admin:
        anims = animation.get_unvalidated_animations()
    else:
        anims = ''
    
    try:
        _path = os.path.join(config.PAGE_DIR, 'notice', 'current.htm')
        with open(_path, 'r') as _pg:
            page = _pg.read()
    except FileNotFoundError:
        _path = os.path.join(config.PAGE_DIR, 'notice', 'current.md')
        with open(_path, 'r') as _pg:
            page = utils.render_page(_pg.read())
    
    return render_template('index.htm', anims=anims, contenu=page)


#Cette fonction permet d'afficher le formulaire d'édition de la notice.
@views.route('/edit', methods=['GET','POST'])
@auth.require_valid_user
def edit_notice():
    if g.user.is_admin:
        _filedir = '%s/%s' % (config.PAGE_DIR, 'notice')
        _filename = '%s/%s/current.md' % (config.PAGE_DIR, 'notice')
        _date_edit = (datetime
                        .datetime
                        .now()
                        .strftime('%d/%m/%Y à %H:%M:%S'))

        if request.method == 'GET':
            try:
                with open(_filename, 'r') as pg:
                    contenu = "".join(pg.readlines())
            except FileNotFoundError:
                contenu = ''

            return render_template(
                    'page_form.htm',
                    nom_page='notice',
                    contenu=contenu) 
        else:
            if not os.path.exists(_filedir):
                os.mkdir(_filedir)
                _log_create = True
            else:
                _log_create = False
                fdatetoday = '%s/rev_%s.md' % (
                        _filedir,
                        datetime.datetime.now().strftime('%Y_%m_%d'))
                delta = datetime.timedelta(days=1)
                fdateprev = '%s/rev_%s.md' % (
                        _filedir,
                        (datetime.datetime.now() - delta).strftime('%Y_%m_%d'))
                if not os.path.exists(fdateprev):
                    _filedest = fdateprev
                else:
                    _filedest = fdatetoday
                shutil.copyfile(_filename, _filedest)
            with open(_filename, 'w') as fp:
                fp.write(request.form['contenu'])
            with open(os.path.join(_filedir, 'current.htm'), 'w') as fp:
                _html_content = utils.render_page(request.form['contenu'])
                fp.write(_html_content)
            if not _log_create:
                send_mail(
                    'La page %s a été modifiée' % 'notice',
                    render_template('mail_pages.htm', 
                        pagename='notice')
                    )
            else:
                send_mail(
                    'La page %s a été créée' % 'notice',
                    render_template('mail_pages.htm', 
                        pagename='notice'))
            return redirect('/')
        return redirect('/')


#Cette fonction permet d'afficher le formulaire de connexion.
@views.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'GET':
        err = request.args.get('err', False)
        return render_template('login.htm', err=err)

    login = request.form['login'].strip()
    passwd = request.form['passwd'].strip()
    if request.args.get('url', False):
        redir_page = request.args.get('url')
    else:
        redir_page = url_for('main.index')

    try:
        user = auth.check_ldap_auth(login, passwd)

        serializer = TimedSerializer(config.SECRET_KEY)
        cookie_data = serializer.dumps(user.as_dict())
        cookie_exp = datetime.datetime.now() + datetime.timedelta(days=1)

        resp = current_app.make_response(redirect(redir_page))
        resp.set_cookie('user', cookie_data, expires=cookie_exp)

        return resp
    except auth.InvalidAuthError:
        return redirect(url_for('main.login_view', err=True))


#Cette fonction permet de déconnecter l'utilisateur.
@views.route('/logout')
@auth.require_valid_user
def logout_view():
    resp = current_app.make_response(redirect(url_for('main.index')))
    resp.set_cookie('user', '')
    return resp


#Cette fonction permet de récupérer les statistiques du nombre d'animations
#et de médias au cours du temps.
@views.route('/get_stats')
@auth.require_valid_user
def get_stats():
    dates = []

    current_date = date.today()
    while date(2022, 5, 1) < current_date:
        dates.append(current_date.isoformat())
        current_date = current_date.replace(day=1) - timedelta(days=1)
    dates.reverse()

    all_anims_stats = []
    all_animations = animation.get_all_animations()

    valid_anims_stats = []
    valid_animations = animation.get_validated_animations()

    unvalid_anims_stats = []
    unvalid_animations = animation.get_unvalidated_animations()
    
    mat_pedas_stats = []
    mat_pedas = mat_peda.select_medias()

    outils_stats = []
    outils = mat_peda.select_all_outils()
    
    for item in dates:

        all_anim_compte = 0
        for anim in all_animations:
            if anim.date_modif <= date.fromisoformat(item):
                all_anim_compte+=1
        all_anims_stats.append(all_anim_compte)

        valid_anim_compte = 0
        for anim in valid_animations:
            if anim.date_modif <= date.fromisoformat(item):
                valid_anim_compte+=1
        valid_anims_stats.append(valid_anim_compte)

        unvalid_anim_compte = 0
        for anim in unvalid_animations:
            if anim.date_modif <= date.fromisoformat(item):
                unvalid_anim_compte+=1
        unvalid_anims_stats.append(unvalid_anim_compte)

        mat_peda_compte = 0
        for mat in mat_pedas:
            if mat.date_modif <= date.fromisoformat(item):
                mat_peda_compte+=1
        mat_pedas_stats.append(mat_peda_compte)

        outil_compte = 0
        for outil in outils:
            if outil.date_modif <= date.fromisoformat(item):
                outil_compte+=1
        outils_stats.append(outil_compte)

    response = {
        'dates':dates, 'y_anim_all':all_anims_stats, 'y_anim_valid':valid_anims_stats, 'y_anim_unvalid':unvalid_anims_stats, 
        'y_mat_peda':mat_pedas_stats, 'y_outil':outils_stats
    }

    return json.dumps(response)


#Cette fonction permet d'afficher les pages 
#d'outils facilitateurs pour le layout
@views.route('/get_outils')
@auth.require_valid_user
def get_outils_pagenames():
    types_outils = thesaurus.get_from_thes(nom='ref.type_outil')
    return json.dumps([[item.label, item.nom] for item in types_outils])