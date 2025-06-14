import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
          surface: '#FFFFFF',
          'surface-variant': '#F5F5F5',
          background: '#F5F5F5',
        },
      },
      dark: {
        colors: {
          primary: '#2196F3',
          secondary: '#424242',
          surface: '#121212',
          'surface-variant': '#1E1E1E',
          background: '#121212',
        },
      },
    },
  },
})

const app = createApp(App)
app.use(vuetify)
app.use(router)
app.mount('#app')
