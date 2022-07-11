<script>
	
export default {
	name: 'seqform',
	props: ['parties','approches','modalites','durees', 'medias', 'types_mat', 'thematiques', 'idx', 'data'],
	data () {
		return {
			reduction: false,
			open: false,
			type_mat_filters: [],
			theme_filters: []
		}
	},
	methods: {
		toggle () {
			this.open = !this.open;
			if (this.open) {
				this.$emit('get-medias')
			}
		},
		toggle_media (media) {
			media.open = !media.open
		},
		get_icon (type_mat_id) {
			if (type_mat_id==70) {
				return 'image icon'
			} else if (type_mat_id==71) {
				return 'camera icon'
			} else if (type_mat_id==72) {
				return 'video icon'
			} else if (type_mat_id==73) {
				return 'volume up icon'
			} else if (type_mat_id==74) {
				return 'file icon'
			} else if (type_mat_id==75) {
				return 'book icon'
			} else {
				return ''
			}
		},
		get_url (media) {
			return '/' + media.url
		},
		get_ressource_url (ressource_id) {
			let ressource_nom = this.thematiques.filter(e => {return e.id==ressource_id})[0].nom;
			return '/static/ressources/' + ressource_nom + '.png'
		},
		get_ressource_nom (ressource_id) {
			return this.thematiques.filter(e => {return e.id==ressource_id})[0].nom;
		},
		add_materiel (media_id) {
			this.data.materiel.push(media_id)
		},
		remove_materiel (media_id) {
			this.data.materiel.splice(this.data.materiel.indexOf(media_id), 1)
		},
		get_media_nom (media_id) {
			return this.medias.filter(e => {return e.id == media_id})[0].nom
		},
		get_tag_id (id) {
			return this.idx+'seq'+id
		}
	},
	computed: {
		getcolor () {
			if (this.data.fk_type_seq==42) {
				return 'intro-color'
			} else if (this.data.fk_type_seq==43) {
				return 'dvp-color'
			} else if (this.data.fk_type_seq==44) {
				return 'dvpopt-color'
			} else if (this.data.fk_type_seq==45) {
				return 'conclu-color'
			} else {
				return 'grey inverted'
			}
		},
		getfilteredmedias () {
			let first_filter = this.medias
			if (this.type_mat_filters.length!=0) {
				first_filter = first_filter.filter(e => {return this.type_mat_filters.includes(e.fk_type_mat)})
			}

			let second_filter = first_filter;
			if (this.theme_filters.length!=0) { 
				for (let theme in this.theme_filters) {
					second_filter = second_filter.filter(e => {return e.thematiques.includes(this.theme_filters[theme])})
				}
			}
			return second_filter
		}
	}
}

</script>

<template>
	<div>
		<div v-if="reduction">
			<div class="ui fluid segment" :class="getcolor" style="margin-bottom: 10px;">
				<p class="ui center aligned header">{{data.titre}}</p>
				<button @click="reduction=false" type="button" class="ui primary button fluid">Augmenter la séquence</button>
			</div>
		</div>
		<div v-else>
			<div class="ui segments" style="margin-bottom: 10px;">
				<div class="ui segment fluid labeled input">
					<select class="ui compact selection dropdown" name="partie" id="partie" v-model="data.fk_type_seq">
						<option value="">Choisir ...</option>
						<option v-for="partie in parties" :value="partie['id']">{{partie['nom']}}</option>
					</select>
					<label class="ui label">Titre*</label>
					<input type="text" name="titre" v-model="data.titre">
					<button @click="reduction=true" type="button" class="ui primary button">Réduire la séquence</button>
					<button type="button" @click="$emit('remove-seq')" class="circular ui icon red button" style="margin-left: 10px;"><i class="x icon"></i></button>
				</div>
				<div class="ui horizontal segments">
					<div style="width: 50%;" class="ui container segment" :class="getcolor">
						<b style="margin-right: 10px;">Approche et modalités*</b>
						<select style="width: 30%" class="ui floated compact selection dropdown" name="approche" v-model="data.fk_approche">
							<option value="">Choisir ...</option>
							<option v-for="approche in approches" :value="approche['id']">{{approche['nom']}}</option>
						</select>
						<select style="width: 30%" class="ui floated compact selection dropdown" name="modalite" v-model="data.fk_modalite">
							<option value="">Choisir ...</option>
							<option v-for="modalite in modalites" :value="modalite['id']">{{modalite['nom']}}</option>
						</select>
					</div>
					<div style="width: 50%;" class="ui container segment" :class="getcolor">
						<b style="margin-right: 10px;">Durée*</b>
						<select style="width: 40%" class="ui floated compact selection dropdown" name="duree" v-model="data.fk_duree">
							<option value="">Choisir ...</option>
							<option v-for="duree in durees" :value="duree['id']">{{duree['nom']}}</option>
						</select>
					</div>
				</div>
				<div class="ui horizontal segments">
					<div style="width: 50%;" class="ui container segment" :class="getcolor"><p><b>Description de l'animation par les séquences*</b></p></div>
					<div style="width: 35%;" class="ui container segment" :class="getcolor"><p><b>Objectifs*</b></p></div>
					<div style="width: 15%;" class="ui container segment" :class="getcolor"><p><b>Matériel</b></p></div>
				</div>
				<div class="ui horizontal segments">
					<textarea style="resize: vertical; width: 50%;" rows="7" class="ui segment" name="description" v-model="data.description"></textarea>
					<textarea style="resize: none; width: 35%;" class="ui segment" name="objectifs" v-model="data.objectifs"></textarea>
					<textarea style="resize: none; width: 15%" class="ui segment" name="materiel" v-model="data.materiel_div"></textarea>
				</div>
				<div class="ui segment" style="width: 100%">
						<div style="width: 100%;" class="ui container">
							<sui-button @click.native="toggle">Sélectionner un média</sui-button>
							<sui-modal v-model="open" :closable="false">
								<sui-modal-header>
									Sélectionnez un ou plusieurs médias
								</sui-modal-header>
								<sui-modal-content scrolling style="height: 80vh;">
									<div class="ui grid">
										<div class="row">
											<div class="three wide column" style="position: fixed; width: 20%;">
												<p>Types de médias :</p>
												<div class="grouped field" style="margin-bottom: 15px;">
													<div class="field" v-for="type in types_mat">
														<div class="ui checkbox mini-right-margin">
															<input type="checkbox" :value="type['id']" :id="get_tag_id(type['id'])" v-model="type_mat_filters">
															<label :for="get_tag_id(type['id'])">{{type['nom']}}</label>
														</div>
													</div>
												</div>
												<p>Thématiques :</p>
												<div class="grouped field" style="margin-bottom: 15px;">
													<div class="field" v-for="theme in thematiques">
														<div class="ui checkbox mini-right-margin">
															<input type="checkbox" :value="theme['id']" :id="get_tag_id(theme['id'])" v-model="theme_filters">
															<label :for="get_tag_id(theme['id'])">{{theme['nom']}}</label>
														</div>
													</div>
												</div>
											</div>
											<div class="thirteen wide column" style="margin-left: 20%;">
												<div class="ui clearing segment" v-for="media in getfilteredmedias">
													<i :class="get_icon(media.fk_type_mat)"></i>
													{{media.nom}}
													<button v-if="!data.materiel.includes(media.id)" @click="add_materiel(media.id)" type="button" class="circular ui icon green button right floated" style="margin-left: 10px;"><i class="plus icon"></i></button>
													<button v-else @click="remove_materiel(media.id)" class="circular ui icon red button right floated" style="margin-left: 10px;"><i class="x icon"></i></button>
													<sui-button @click.native="toggle_media(media)" floated="right">Aperçu</sui-button>
													<i v-for="theme in media.thematiques" class="ui icon tooltip right floated">
														<img class="ui mini image" :src="get_ressource_url(theme)">
														<span class="tooltiptext">{{get_ressource_nom(theme)}}</span>
													</i>
													<sui-modal v-if="media.open" v-model="media.open" :closable="false">
														<sui-modal-header>
															{{media.nom}}
														</sui-modal-header>
														<sui-modal-content style="height: 80vh;">
															<video v-if="media.fk_type_mat==72" controls class="big-embed" >
																<source :src="get_url(media)">
																Votre navigateur ne supporte pas cette extension.
															</video>
															<audio v-else-if="media.fk_type_mat==73" controls class="big-embed">
																<source :src="get_url(media)">
																Votre navigateur ne supporte pas cette extension.
															</audio>
															<embed v-else :src="get_url(media)" class="big-embed"></embed>
														</sui-modal-content>
														<sui-modal-actions>
															<sui-button positive @click.native="toggle_media(media)">OK</sui-button>
														</sui-modal-actions>
													</sui-modal>
												</div>
											</div>
										</div>
									</div>
								</sui-modal-content>
								<sui-modal-actions>
									<sui-button positive @click.native="toggle">OK</sui-button>
								</sui-modal-actions>
							</sui-modal>
							<button v-for="media in data.materiel" @click="remove_materiel(media)" class="ui button" style="margin-top: 5px;"><i class="x red icon"></i>{{get_media_nom(media)}}</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>