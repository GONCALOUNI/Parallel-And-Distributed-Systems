import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/dark-mode.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

function applyTheme(theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark')
}

const saved = localStorage.getItem('theme')
if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  applyTheme('dark')
} else {
  applyTheme('light')
}

const app = createApp(App)
app.use(router)
app.mount('#app')