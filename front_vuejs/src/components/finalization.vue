<script>
	
export default {
	name: 'final_form',
	props: ['lieux', 'thematiques', 'saisons', 'publics','data'],
	computed: {
		dvl () {return this.data.description.length},
		pvl () {return this.data.public_specifique.length}
	},
	methods: {
		MaxLengthTextarea(valuename, maxlength){
			if (this.data[valuename].length > maxlength) {
				this.data[valuename] = this.data[valuename].substring(0, maxlength);
				alert('Votre texte ne doit pas dépasser '+maxlength+' caractères!');
			}
		}
	}

}

</script>

<template>
	<div>
		<div class="ui segments" style="margin-bottom: 10px;">
			<div class="ui horizontal segments">
				<div class="ui segment">
					<p>Description* :</p>
					<textarea required style="resize: vertical; box-sizing: border-box; width: 100%;" rows="18" placeholder="Rentrer le texte en moins de 400 caractères." v-model="data.description" name="description" @keyup="MaxLengthTextarea('description', 400)"></textarea>
					<p>{{dvl}}</p>
				</div>
				<div class="ui segment">
					<p>Public spécifique :</p>
					<textarea style="resize: vertical; box-sizing: border-box; width: 100%;" rows="18" placeholder="Rentrer le texte en moins de 400 caractères." name="public_specifique" v-model="data.public_specifique"  @keyup="MaxLengthTextarea('public_specifique', 400);"></textarea>
					<p>{{pvl}}</p>
				</div>
			</div>
			<div class="ui segment">
				<p>Mots-clés* :</p>
				<div class="ui segment">
					<p>Thématiques :</p>
					<div class="ui checkbox mini-right-margin" v-for="thematique in thematiques">
						<input type="checkbox" :value="thematique['id']" :id="thematique['id']" v-model="data.tags">
						<label :for="thematique['id']">{{thematique['nom']}}</label>
					</div>
				</div>
				<div class="ui segment">
					<p>Lieux :</p>
					<div class="ui checkbox mini-right-margin" v-for="lieu in lieux">
						<input type="checkbox" :value="lieu['id']" :id="lieu['id']" v-model="data.tags">
						<label :for="lieu['id']">{{lieu['nom']}}</label>
					</div>
				</div>
				<div class="ui segment">
					<p>Saisons :</p>
					<div class="ui checkbox mini-right-margin" v-for="saison in saisons">
						<input type="checkbox" :value="saison['id']" :id="saison['id']" v-model="data.tags">
						<label :for="saison['id']">{{saison['nom']}}</label>
					</div>
				</div>
				<div class="ui segment">
					<p>Public :</p>
					<div class="ui checkbox mini-right-margin" v-for="_public in publics">
						<input type="checkbox" :value="_public['id']" :id="_public['id']" v-model="data.tags">
						<label :for="_public['id']">{{_public['nom']}}</label>
					</div>
				</div>
			</div>
			<div class="ui segment">
				<p><div>
					<p>Après l'animation :
						<i class="ui question circle outline icon tooltip right floated">
							<span class="tooltiptext-right">Étape(s) à réaliser en aval de l'animation. Ex : vérifier des pièges photos entre deux séances.</span>
						</i>
					</p>
					<textarea style="resize: vertical; box-sizing: border-box; width: 100%;" name="post_anim" v-model="data.post_anim"></textarea>
				</div></p>
			</div>
		</div>
	</div>
</template>