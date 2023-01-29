/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import axios from '@/plugins/axios'
import VCurrencyInput from '@/components/VCurrencyInput'

const app = createApp(App)

registerPlugins(app)

app.provide('axios', axios)

app.component('VCurrencyInput', VCurrencyInput)

app.mount('#app')
