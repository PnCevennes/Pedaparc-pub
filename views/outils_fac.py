import datetime
import shutil
import os
import os.path

from flask import (
        Blueprint,
        render_template,
        send_from_directory,
        redirect,
        url_for,
        request,
        g)

import config

import utils
from utils.auth import require_valid_user, require_admin_user
from utils.mail import send_mail

from werkzeug.utils import secure_filename

from utils import py3o_render

from models.thesaurus import utils as thesaurus
from models.mat_peda import utils as mat_peda

views = Blueprint('outils_facilitateurs', __name__)


#Cette fonction permet d'afficher la page demandée
@views.route('/<pagename>', methods=['GET'])
@require_valid_user
def page(pagename):
    try:
        try:
            _path = os.path.join(config.PAGE_DIR, pagename, 'current.htm')
            with open(_path, 'r') as _pg:
                page = _pg.read()
        except FileNotFoundError:
            _path = os.path.join(config.PAGE_DIR, pagename, 'current.md')
            with open(_path, 'r') as _pg:
                page = utils.render_page(_pg.read())
        return render_template(
                'outils_facilitateurs/page.htm',
                contenu=page,
                pagename=pagename,
                documents=mat_peda.get_outils(pagename))
    except FileNotFoundError:
        return render_template('outils_facilitateurs/404.htm', 
            pagename=pagename)


#Cette fonction permet d'editer la page correspondante
@views.route('/<pagename>/edit', methods=['GET', 'POST'])
@require_valid_user
@require_admin_user
def edit_page(pagename):
    _filedir = '%s/%s' % (config.PAGE_DIR, pagename)
    _filename = '%s/%s/current.md' % (config.PAGE_DIR, pagename)
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
            nom_page=pagename,
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
                'La page %s a été modifiée' % pagename,
                render_template('outils_facilitateurs/mail_pages.htm', 
                    pagename=pagename)
                )
        else:
            send_mail(
                'La page %s a été créée' % pagename,
                render_template('outils_facilitateurs/mail_pages.htm', 
                    pagename=pagename))
        return redirect(url_for('outils_facilitateurs.page', 
            pagename=pagename))
    return redirect('/')

#Cette fonction permet de render le form de création d'un nouvel outil
@views.route('/create', methods=['GET'], strict_slashes=False)
@require_valid_user
def outils_facilitateurs_create_form():
    return render_template('/outils_facilitateurs/outils_create_form.htm', 
        types_outils = thesaurus.get_from_thes(code='ref.type_outil'),
        types_medias = thesaurus.get_from_thes(code='ref.type_mat'),
        difficultes = thesaurus.get_from_thes(code='ref.difficulte'))


#Cette fonction permet de vérifier si 
#le fichier upload à une extension autorisée
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


#Cette fonction permet de créer le media à partir du form rempli
@views.route('/create', methods=['POST'])
@require_valid_user
def outils_facilitateurs_create():
    file = request.files['file']
    data = dict(request.form)
    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            data['url'] = os.path.join(config.UPLOAD_FOLDER, filename)
            file.save(data['url'])
        else:
            return render_template('/outils_facilitateurs/outils_create_form.htm', 
                types = thesaurus.get_from_thes(code='ref.type_outil'),
                difficultes = thesaurus.get_from_thes(code='ref.difficulte'), 
                alert=config.ALLOWED_EXTENSIONS)
    else:
        data['url'] = ''

    mat_peda.create_outil(data)
        
    return redirect(url_for('outils_facilitateurs.page', pagename=thesaurus.get_thesaurus(data['type_outil']).code))


#Cette fonction permet de supprimer l'outil concerné
@views.route('/<pagename>/<id_document>/delete', methods=['GET'])
@require_valid_user
@require_admin_user
def outils_facilitateur_delete_outil(pagename, id_document):
    mat_peda.delete_mat_peda(id_document)
    return redirect(url_for('outils_facilitateurs.page', 
            pagename=pagename))


#Cette fonction permet d'afficher le form de mise à jour d'un outil
@views.route('/<pagename>/<id_document>/edit', methods=['GET'])
@require_valid_user
@require_admin_user
def update_outil_page(pagename,id_document):
    return render_template('/outils_facilitateurs/outils_create_form.htm', 
        types = thesaurus.get_from_thes(code='ref.type_outil'), 
        outil = mat_peda.get_mat_peda(id_document),
        difficultes = thesaurus.get_from_thes(code='ref.difficulte'),
        types_medias = thesaurus.get_from_thes(code='ref.type_mat'),
        pagename = pagename)


#Cette fonction permet de mettre à jour un outil
@views.route('/<pagename>/<id_document>/edit', methods=['POST'])
@require_valid_user
@require_admin_user
def update_outil(pagename,id_document):
    data = dict(request.form)
    file = request.files['file']
    document = mat_peda.get_mat_peda(id_document)
    if file:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            old_url = document.url
            if old_url:
                try:
                    os.remove(old_url)
                except Exception as e:
                    pass
            data['url'] = os.path.join(config.UPLOAD_FOLDER, filename)
            file.save(data['url'])
        else:
            return render_template('/outils_facilitateurs/outils_create_form.htm', 
                types = thesaurus.get_from_thes(code='ref.type_outil'),
                difficultes = thesaurus.get_from_thes(code='ref.difficulte'), 
                alert=config.ALLOWED_EXTENSIONS)
    else:
        data['url'] = document.url

    data['id_outil'] = id_document
    mat_peda.update_outil(data)
    return redirect(url_for('outils_facilitateurs.page', 
        pagename=pagename))


#Cette fonction permet de télécharger un outil
@views.route('/<id_document>/download', methods=['GET'])
@require_valid_user
def download_outil(id_document):
    outil = mat_peda.outil_delete_md(mat_peda.get_mat_peda(id_document), 
        py3o_render.md_to_text)

    secure_name = secure_filename(outil.nom)

    path = os.path.join(config.DOWNLOAD_FOLDER, secure_name)

    filename = py3o_render.render_file(
        outil=outil,
        path=path)

    shutil.make_archive(path, 'zip', path)
    shutil.rmtree(path)
    
    return (send_from_directory(config.DOWNLOAD_FOLDER, 
        os.path.basename(secure_name+'.zip'), 
        as_attachment=True), 
        os.remove(path+'.zip'))