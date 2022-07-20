import datetime

from flask import (
        Blueprint,
        render_template,
        redirect,
        request,
        g)

import json
import utils

from models.animation import utils as animation
from models.sequence import utils as sequence
from models.thesaurus import utils as thesaurus
from models.mat_peda import utils as mat_peda

from utils import auth

views = Blueprint('pedatheque_edit',__name__)

#Cette fonction permet de récupérer tous les mots-clés du thesaurus
@views.route('/get_thes', methods=['GET'])
@auth.require_valid_user
def get_thes():
     return json.dumps(
          { thes.nom : [{'id': tag.id, 'nom': tag.nom} for tag in thesaurus.get_from_thes(idref=thes.id)] 
          for thes in thesaurus.get_from_thes(idref=0) }
          )


#Cette fonctions permet de récupérer tous les médias.
@views.route('/get_medias', methods=['GET'])
def pedatheque_create_media_search():
     return json.dumps(
          [{
          'id':item.id, 'nom':item.nom, 
          'url':item.url, 'fk_type_mat':item.fk_type_mat.id, 
          'open':False, 'thematiques':[theme.id for theme in item.thematiques[:]]
          } for item in mat_peda.get_all_medias()])


#Cette fonction permet d'appeler le formulaire de la première étape de création
#d'un animation
@views.route('/', methods=['GET'], strict_slashes=False)
@auth.require_valid_user
def pedatheque_create_create_form():
     if 'q' not in request.args:
          return render_template('/pedatheque/create/anim_create_form.htm', data='')
     else:
          data = animation.anim_to_dict(request.args['q'])
          return render_template('/pedatheque/create/anim_create_form.htm', data=data)


#Cette fonction permet la création ou la mise à jour d'une animation
@views.route('/cr_or_up_anim', methods=['POST'])
def create_or_update_animation():
     data = request.json
     sequences = data.pop('sequences')
     tags = data.pop('tags')
     anim = data
     anim['user'] = g.user.name
     anim['date_modif'] = datetime.datetime.now()

     id_anim = animation.create_or_update_animation(anim, tags)
     sequence.create_or_update_all_sequences(id_anim, sequences)

     return '/pedatheque/'+id_anim