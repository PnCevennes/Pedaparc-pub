import os.path

from flask import (
        Blueprint,
        render_template,
        send_from_directory,
        redirect,
        request,
        g)

from werkzeug.utils import secure_filename
import hashlib
import glob

import utils
import config
from utils import auth

from models.thesaurus import utils as thesaurus
from models.mat_peda import utils as mat_peda

views = Blueprint('mediatheque',__name__)


#Cette fonction permet de render le form d'import de média
@views.route('/create', methods=['GET'])
@auth.require_valid_user
def mediatheque_create_form():
    return render_template('/mediatheque/create/media_form.htm', 
            types = thesaurus.get_from_thes(nom='ref.type_mat'), 
            thematiques = thesaurus.get_from_thes(nom='ref.thematiques'))


#Cette fonction permet de vérifier si 
#le fichier upload à une extension autorisée
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


#Cette fonction permet de renvoyer la somme md5 du fichier upload
def hash_file(file):
    md5_hash = hashlib.md5(file.read()).hexdigest()
    file.stream.seek(0) 
    return md5_hash


#Cette fonction permet de créer/importer le média
@views.route('/create', methods=['POST'])
@auth.require_valid_user
def mediatheque_create():    
    file = request.files['file']
    if file and allowed_file(file.filename):

        md5_hash = hash_file(file)

        if glob.glob(os.path.join(config.UPLOAD_FOLDER, md5_hash)+'_*'):
            return render_template('/mediatheque/create/media_form.htm', 
                types = thesaurus.get_from_thes(nom='ref.type_mat'), 
                thematiques = thesaurus.get_from_thes(nom='ref.thematiques'), 
                alert='duplicate')

        filename = md5_hash + '_' + secure_filename(file.filename)
        
        data = dict(request.form)
        data['url'] = os.path.join(config.UPLOAD_FOLDER, filename)
        data['thematique'] = request.form.getlist('thematique')
        mat_peda.create_mat_peda(data)
        file.save(data['url'])
        return redirect('/mediatheque')
    else:
        return render_template('/mediatheque/create/media_form.htm', 
            types = thesaurus.get_from_thes(nom='ref.type_mat'), 
            thematiques = thesaurus.get_from_thes(nom='ref.thematiques'), 
            alert=config.ALLOWED_EXTENSIONS)


#Cette fonction permet de render le form d'édit du média
@views.route('/<id_media>/edit', methods=['GET'])
@auth.require_valid_user
@auth.require_admin_user
def mediatheque_edit_form(id_media):
    return render_template('/mediatheque/create/media_form.htm', 
        types = thesaurus.get_from_thes(nom='ref.type_mat'), 
        thematiques = thesaurus.get_from_thes(nom='ref.thematiques'),
        media = mat_peda.get_mat_peda(id_media))


#Cette fonction permet d'éditer le média avec les nouvelles données
@views.route('/<id_media>/edit', methods=['POST'])
@auth.require_valid_user
@auth.require_admin_user
def mediatheque_edit(id_media):
    data = dict(request.form)
    data['id_media'] = id_media
    data['thematique'] = request.form.getlist('thematique')
    mat_peda.update_media(data)
    return redirect('/mediatheque/results?precision=100')


#Cette fonction permet de render la page de recherche des medias 
#avec tags et pertinance
@views.route('/', strict_slashes=False, methods=['GET'])
@auth.require_valid_user
def mediatheque_search():
    tags = {item: thesaurus.get_from_thes(nom=item.nom) for item 
        in utils.format('msearch', thesaurus.get_from_thes('ref'))}
    return render_template('/tags_form.htm', tags=tags, 
        action='mediatheque')


#Cette fonction permet de récupérer les medias 
#qui matchent la recherche et affiche les résultats
@views.route('/results', methods=['GET'])
@auth.require_valid_user
def mediatheque_results():
    types = request.args.getlist('ref.type_mat')
    tags = request.args.getlist('ref.thematiques')
    
    match = mat_peda.match_mat_peda_tags(types,tags)
    
    return render_template('/mediatheque/search/results.htm', medias=match)


#Cette fonction permet de télécharger le média
@views.route('/<id_media>', methods=['GET'])
@auth.require_valid_user
def mediatheque_download(id_media):
    return send_from_directory(config.UPLOAD_FOLDER, 
        os.path.basename(mat_peda.get_mat_peda(id_media).url), as_attachment=True)


#Cette fonction permet de supprimer le média concerné
@views.route('/<id_media>/delete', methods=['GET'])
@auth.require_valid_user
@auth.require_admin_user
def mediatheque_delete(id_media):
    mat_peda.delete_mat_peda(id_media)
    return redirect('/mediatheque/results?precision=100')