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

import { defineRule, configure } from 'vee-validate'
import { required, max, min } from "@vee-validate/rules"
import { localize } from '@vee-validate/i18n';
import en from '@vee-validate/i18n/dist/locale/en.json';

defineRule('required', required)
defineRule('min', min)
defineRule('max', max)

configure({
    validateOnChange: true,
    validateOnModelUpdate: false,
    generateMessage: localize({ en }),
});


const app = createApp(App)

registerPlugins(app)

app.provide('axios', axios)

app.component('VCurrencyInput', VCurrencyInput)

app.mount('#app')
