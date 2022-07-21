'''
Fichier contenant les fonctions utiles à la manipulation des mat_peda.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fonctions:

   | create_media(data) -> Mat_peda
   | create_outil(data) -> Mat_peda
   | update_media(data)
   | update_outil(data)
   | match_mat_peda_tags(types, tags) -> [Mat_peda, pertinence][]
   | get_all_mat_pedas() -> Mat_peda[]
   | get_all_medias() -> Mat_peda[]
   | get_all_outils() -> Mat_peda[]
   | get_outils(code) -> Mat_peda[]
   | get_mat_peda(id_media) -> Mat_peda
   | delete_mat_peda(id_media)
   | outil_delete_md(outil, md_to_text) -> Mat_peda
'''

from peewee import fn

from models.mat_peda.mat_peda import Mat_peda, Rel_mat_peda_sequence, Rel_mat_peda_thematique
from models.thesaurus.thesaurus import Thesaurus
from models.thesaurus.utils import get_from_thes

#====================Mat_peda====================#

def create_media(data):
	'''
	Crée un objet Mat_peda (média) à partir des données passées en paramètre.

		Param(s):
				| data ({}): Dictionnaire contenant les attributs de l'objet (média)

		Return(s):
				| mat_peda (Mat_peda): Objet Mat_peda (média) dont les attributs ont été remplis
	'''
	mat_peda = Mat_peda.create(
		fk_type_mat = Thesaurus.get(id=data['type_mat']),
		nom = data['nom'],
		description = data['description'],
		url = data['url'])
	for item in data['thematique']:
		Rel_mat_peda_thematique.create(fk_mat_peda=mat_peda, fk_thes=Thesaurus.get(id=item))
	return mat_peda


def create_outil(data):
	'''
	Crée un objet Mat_peda (outil facilitateur) à partir des données
	passées en paramètre.

		Param(s):
				| data ({}): Dictionnaire contenant les attributs de l'objet (outil facilitateur)

		Return(s):
				| outil (Mat_peda): Objet Mat_peda (outil facilitateur) dont les attributs ont été remplis
	'''
	outil = Mat_peda.create(
		fk_type_mat = Thesaurus.get(id=data['type_outil']),
		nom = data['nom'],
		description = data['description'],
		variante = data['variante'],
		difficulte = Thesaurus.get(id=data['difficulte']),
		materiel = data['materiel'],
		url = data['url'],
		fk_type_mat_outil = Thesaurus.get(id=data['type_media']) if data['url'] else Thesaurus.get(id=2))
	return outil


def update_media(data):
	'''
	Met à jour les données de l'objet Mat_peda à partir
	d'un Dictionnaire contenant les nouvelles données et
	met à jour les mots-clés Thesaurus associés.

		Param(s):
				| data ({}): Dictionnaire contenant les nouveaux attributs de l'objet et les nouvelles thématiques
	'''
	media = Mat_peda.get(id=data['id_media'])
	
	Rel_mat_peda_thematique.delete().where(Rel_mat_peda_thematique.fk_mat_peda==media.id).execute()

	media.fk_type_mat = Thesaurus.get(id=data['type_mat'])
	media.nom = data['nom']
	media.description = data['description']
	media.save()

	for item in data['thematique']:
		Rel_mat_peda_thematique.create(fk_mat_peda=media, fk_thes=Thesaurus.get(id=item))


def update_outil(data):
	'''
	Met à jour les données de l'objet Mat_peda à partir
	d'un Dictionnaire contenant les nouvelles données

		Param(s):
				| data ({}): Dictionnaire contenant les nouveaux attributs de l'objet
	'''
	outil = Mat_peda.get(id=data['id_outil'])
	outil.nom = data['nom']
	outil.description = data['description']
	outil.variante = data['variante']
	outil.difficulte = Thesaurus.get(id=data['difficulte'])
	outil.materiel = data['materiel']
	outil.url = data['url']
	outil.fk_type_mat_outil = Thesaurus.get(id=data['type_media']) if data['url'] else Thesaurus.get(id=2) 
	outil.save()


def mat_peda_sort(tab):
   return tab[1]


def mat_peda_sort_alpha(tab):
	return tab[0].nom


def match_mat_peda_tags(types, tags):
	'''
	Retourne tous les objets Mat_peda correspondants aux mots-clés et
	types passés en paramètre.

		Param(s):
				| types (Thesaurus[]): Liste d'objets Thesaurus à utiliser pour la recherche
				| tags (Thesaurus[]): Liste d'objets Thesaurus à utiliser pour la recherche

		Return(s):
				| mat_pedas ([Mat_peda, pertinence][]): Liste de tous les objets Mat_peda correspondant aux mots-clés et types donnés.
	'''

	if not types:
		types = [item.id for item in get_from_thes(code='ref.type_mat')]

	queryTypes = Mat_peda.select().where(Mat_peda.fk_type_mat.in_(types))

	if tags:
		query = list(
			Rel_mat_peda_thematique.select(Rel_mat_peda_thematique.fk_mat_peda.alias('mat_peda'), fn.COUNT(Rel_mat_peda_thematique.fk_mat_peda).alias('count')).where(
				Rel_mat_peda_thematique.fk_mat_peda.in_(queryTypes) & Rel_mat_peda_thematique.fk_thes.in_(tags)
				).group_by(Rel_mat_peda_thematique.fk_mat_peda).dicts()
			)
	else:
		query = [{'mat_peda': item.id} for item in queryTypes]

	match = [[Mat_peda.get(id=item['mat_peda']), (str(item['count'])+'/'+str(len(tags)) if len(tags) else '')] 
	for item in query]

	if not tags:
		return sorted(match, key=mat_peda_sort_alpha, reverse=False)
	else:
		return sorted(match, key=mat_peda_sort, reverse=True)


def get_all_mat_pedas():
	'''
	Retourne tous les objets Mat_peda sans distinctions.

		Return(s):
				| mat_pedas (Mat_peda[]): Liste de tous les objets Mat_peda
	'''
	return Mat_peda.select()[:]


def get_all_medias():
	'''
	Retourne tous les objets Mat_peda étant des médias.

		Return(s):
				| mat_pedas (Mat_peda[]): Liste de tous les objets Mat_peda (médias)
	'''
	return [item for item in Mat_peda.select() if item.fk_type_mat in get_from_thes(code='ref.type_mat')]


def get_all_outils():
	'''
	Retourne tous les objets Mat_peda étant des outils facilitateurs.

		Return(s):
				| mat_pedas (Mat_peda[]): Liste de tous les objets Mat_peda (outils)
	'''
	return [item for item in Mat_peda.select() if item.fk_type_mat in get_from_thes(code='ref.type_outil')]


def get_outils(code):
	'''
	Retourne tous les objets Mat_péda étant des outils facilitateurs d'une catégorie d'outils.

		Param(s):
				| code (str): Catégorie des outils facilitateurs que l'on veut

		Return(s):
				| mat_pedas (Mat_peda[]): Liste de tous les objets Mat_peda (outil facilitateur)
	'''
	return Mat_peda.select().where(Mat_peda.fk_type_mat==Thesaurus.get(code=code))


def get_mat_peda(id_media):
	'''
	Retourne l'objet Mat_peda dont l'Id est passé en paramètre.

		Param(s):
				| id_media (int): Id de l'objet Mat_peda à retourner

		Return(s):
				| mat_peda (Mat_peda): Objet Mat_peda dont l'Id a été passé en paramètre
	'''
	return Mat_peda.get(id=id_media)


def delete_mat_peda(id_media):
	'''
	Supprime l'objet Mat_peda dont l'Id a été passé en paramètre
	et toutes ses relations.

		Param(s):
				| id_media (int): Id de l'objet à supprimer
	'''
	Rel_mat_peda_thematique.delete().where(Rel_mat_peda_thematique.fk_mat_peda==id_media).execute()
	Rel_mat_peda_sequence.delete().where(Rel_mat_peda_sequence.fk_mat_peda==id_media).execute()
	Mat_peda.delete().where(Mat_peda.id==id_media).execute()


def outil_delete_md(outil, md_to_text):
	'''
	Retourne une copie de l'objet Mat_peda dont le markdown
	des attributs a été retiré.

		Param(s):
				| outil (Mat_peda): Objet Mat_peda dont le markdown doit être retiré des attributs
				| md_to_text (function): Fonction permettant de transformer du markdown en plain text

		Return(s):
				| copie (Mat_peda): Objet Mat_peda dont les attributs ne sont plus écrits en markdown
	'''
	copie = Mat_peda()
	data = vars(outil)['__data__']

	for item in data:
		if not isinstance(data[item], int) or item=='id':
			setattr(copie, item, md_to_text(str(data[item])))
		else:
			setattr(copie, item, Thesaurus.get(id=data[item]))
	return copie
