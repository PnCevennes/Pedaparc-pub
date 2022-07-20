from flask import (
        Blueprint,
        render_template,
        redirect,
        request,
        g)

from models.thesaurus import utils as thesaurus

from utils import auth

views = Blueprint('thesaurus',__name__)


#Cette fonction permet d'afficher le form de création d'un nouveau tag
@views.route('/', strict_slashes=False, methods=['GET'])
@auth.require_valid_user
@auth.require_admin_user
def thesaurus_create_form():
    return render_template('/thesaurus/thesaurus_admin.htm', 
        references = thesaurus.get_from_thes(idref='0'),
        tags = thesaurus.get_all_thes())


#Cette fonction permet de créer le nouveau tag
@views.route('/create', methods=['POST'])
@auth.require_valid_user
@auth.require_admin_user
def thesaurus_create_tag():
    data = request.form
    try:
        thesaurus.create_thesaurus(data)
        return redirect('/')
    except Exception:
        return render_template(
            '/thesaurus/thesaurus_admin.htm',
            references = thesaurus.get_from_thes(idref='0'), 
            alert = data['nom'])


#Cette fonction permet de supprimer un tag
@views.route('/delete', methods=['POST'])
@auth.require_valid_user
@auth.require_admin_user
def thesaurus_delete_tag():
    id_thes = request.form['id_thes']
    thesaurus.delete_thesaurus(id_thes)
    return redirect('/')