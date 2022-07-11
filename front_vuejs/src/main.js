import Vue from 'vue'
import VueCompositionAPI, { createApp, h } from '@vue/composition-api'
import 'semantic-ui-css/semantic.min.css'

import App from './App.vue'

Vue.use(VueCompositionAPI)
Vue.use(SemanticUIVue)

const app = createApp({
  render: () => h(App)
})

app.mount('#app')
