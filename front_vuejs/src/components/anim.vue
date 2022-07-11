<script>
export default {
	name:'animform',
	props: ['durees','data']
}
</script>

<template>
	<div style="margin-bottom: 10px;"> 
		<p>Les champs marqués d'un astérisque (*) sont obligatoires.</p>
		<div class="ui labeled input">
			<label class="ui label">Titre*</label>
			<input type="text" name="titre" v-model="data.titre">
		</div>
		<div class="ui segments">
			<div class="ui segment">
				<p><div class="ui labeled input">
					<label class="ui label">Lieu*</label>
					<input type="text" name="lieu" v-model="data.lieu">
				</div></p>
			</div>
			<div class="ui segment">
				<p><div>
					<p>Objectifs* :</p>
					<textarea style="resize: vertical; box-sizing: border-box; width: 100%;" name="objectifs" v-model="data.objectifs"></textarea>
				</div></p>
				<p><div class="ui labeled input">
					<label class="ui label">Temps d'animation*</label>
					<select class="ui compact selection dropdown" name="duree" v-model="data.fk_duree">
						<option value="">Choisir ...</option>
						<option v-for="duree in durees" :value="duree['id']">{{duree['nom']}}</option>
					</select>
				</div></p>
				<p><div>
					<p>Avant l'animation :
						<i class="ui question circle outline icon tooltip right floated">
							<span class="tooltiptext">Étape(s) à réaliser concrètement en amont de l'animation afin d'en assurer le bon déroulement. Ex : placer des indices sur le terrain avant une chasse au trésor.</span>
						</i>
					</p>
					<textarea style="resize: vertical; box-sizing: border-box; width: 100%;" name="pre_anim" v-model="data.pre_anim"></textarea>
				</div></p>
			</div>
		</div>
	</div>
</template>