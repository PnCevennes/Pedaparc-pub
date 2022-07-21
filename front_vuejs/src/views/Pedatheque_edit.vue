<script>

import Anim from '@/components/anim.vue'
import Seq from '@/components/seq.vue'
import Final from '@/components/finalization.vue'

export default {
	name: 'edit_form',
	components: {Anim, Seq, Final},
	data () {
		return {
			rep: {},
			data: {
				titre: '',
				lieu: '',
				objectifs: '',
				fk_duree: '',
				pre_anim: '',
				post_anim: '',
				description: '',
				public_specifique: '',
				tags: [],
				sequences: []
			},
			medias: [],
			redirect: '',
			end: false,
			global_values: {}
		}
	},
	methods: {
		get_thes () {
			fetch('http://127.0.0.1:5000/pedatheque_edit/get_thes').then(resp => {resp.json().then(data => {this.rep = data; this.set_global();})})
		},
		get_medias () {
			fetch('http://127.0.0.1:5000/pedatheque_edit/get_medias').then(resp => {resp.json().then(data => {this.medias = data; this.medias.sort(function (a, b) {
				if (a.nom==b.nom) {
					return 0;
				} else {
					let compare = [a.nom.toLowerCase(), b.nom.toLowerCase()];
					compare.sort();
					return compare[0] == a.nom.toLowerCase() ? -1 : 1;
				}
			});})})
		},
		add_seq () {
			this.data.sequences.push(
				{
					fk_type_seq: '',
					titre: '',
					description: '',
					fk_approche: '',
					fk_modalite: '',
					objectifs: '',
					fk_duree: '',
					materiel_div: '',
					materiel: []
				}
			);
		},
		remove_seq (idx) {
			this.data.sequences.splice(idx,1)
		},
		send_data (forlater) {
			this.data.statut = forlater ? 3 : 2;
			fetch('/pedatheque_edit/cr_or_up_anim', {
				method: 'POST',
				headers: {
					'Content-Type':'application/json'
				},
				body: JSON.stringify(this.data)
			}).then(resp => {resp.text().then(data => {this.redirect = data; this.end = true;})});
		},
		set_global () {
			this.global_values = {
				'intro':this.find_id_by_code('ref.type_seq','intro'),
				'dvp':this.find_id_by_code('ref.type_seq','dvp'),
				'dvpopt':this.find_id_by_code('ref.type_seq','dvpopt'),
				'conclu':this.find_id_by_code('ref.type_seq','conclu'),
				'image':this.find_id_by_code('ref.type_mat','image'),
				'photo':this.find_id_by_code('ref.type_mat','photo'),
				'video':this.find_id_by_code('ref.type_mat','video'),
				'bandeson':this.find_id_by_code('ref.type_mat','bandeson'),
				'support':this.find_id_by_code('ref.type_mat','support'),
				'conte':this.find_id_by_code('ref.type_mat','conte')
			}
		},
		find_id_by_code (categorie, code) {
			for (let idx in this.rep[categorie]) {
				if (this.rep[categorie][idx]['code']==code) {
					return this.rep[categorie][idx]['id'];
				}
			}
		}
	},
	computed: {
		isfirst () {
			return this.data.sequences.length==0;
		},
		hasconclusion () {
			let bool;
			if (this.data.sequences.length==0) {
				bool = false;
			} else {
				bool = this.data.sequences[this.data.sequences.length-1].fk_type_seq==45;
			}

			if (!bool) {
				this.data.description = '';
				this.data.public_specifique = '';
				this.data.post_anim = '';
				this.data.tags = [];
			}

			return bool;
		},
		animcomplete () {
			return this.data.titre && this.data.lieu && this.data.objectifs && this.data.fk_duree;
		},
		firstseqisintro () {
			if (this.data.sequences.length!=0 && this.data.sequences[0].fk_type_seq!='') {
				if (this.data.sequences[0].fk_type_seq!=42) {
					alert('La première séquence doit être une introduction.');
					this.data.sequences[0].fk_type_seq = 42;					
				}
				return true; 				
			}

		},
		allseqcomplete () {
			for (const key in this.data.sequences) {
				const sequence = this.data.sequences[key];
				if (!sequence.fk_type_seq || !sequence.titre || !sequence.description || !sequence.fk_approche || !sequence.fk_modalite || !sequence.objectifs || !sequence.fk_duree) {
					return false;
				}
			}
			return true;
		},
		finaliscomplete () {
			return this.data.description && this.data.tags.length!=0;
		},
		issend () {
			return this.end;
		}
	},
	mounted () {
		this.get_thes();
		this.get_medias();
		if (document.data) {
			this.data = document.data;
		}
	}
}

</script>

<template>
	<div v-if="!issend" style="width: 80%; margin-bottom: 100px;" class="ui very padded container">
		<Anim :durees="rep['ref.duree']" :data="data"/>
		<button v-if="isfirst && animcomplete" type="button" @click="add_seq" class="ui primary button" style="margin-bottom: 10px;">Première séquence</button>
		<button v-if="isfirst && animcomplete" type="button" class="ui right floated yellow button" @click="send_data(true)">Finir plus tard</button>
		<Seq v-if="animcomplete" v-for="(sequence, idx) in data.sequences" :data="sequence" :key="idx" :idx="idx" :parties="rep['ref.type_seq']" :approches="rep['ref.approches']" :modalites="rep['ref.modalites']" :durees="rep['ref.duree_seq']" :medias="medias" :types_mat="rep['ref.type_mat']" :thematiques="rep['ref.thematiques']" :global_values="global_values" @remove-seq="remove_seq(idx)" @get-medias="get_medias()"/>
		<button v-if="!isfirst && firstseqisintro && allseqcomplete" type="button" @click="add_seq" class="circular ui icon primary button" style="margin-bottom: 10px;"><i class="plus icon"></i></button>
		<button v-if="!isfirst && firstseqisintro && allseqcomplete && !hasconclusion" type="button" class="ui right floated yellow button" @click="send_data(true)">Finir plus tard</button>
		<Final v-if="hasconclusion && allseqcomplete" :data="data" :thematiques="rep['ref.thematiques']" :lieux="rep['ref.lieux']" :saisons="rep['ref.saison']" :publics="rep['ref.public']"/>
		<button v-if="hasconclusion && animcomplete && allseqcomplete && finaliscomplete" type="button" class="ui primary button" @click="send_data(false)">Envoyer</button>
		<button v-if="hasconclusion && animcomplete && allseqcomplete && !finaliscomplete" type="button" class="ui right floated yellow button" @click="send_data(true)">Finir plus tard</button>
	</div>
	<div v-else style="margin-top: 100px;">
		<h1 class="ui center aligned header">Vous pouvez consulter <a :href="redirect">votre animation</a> !</h1>
	</div>
</template>