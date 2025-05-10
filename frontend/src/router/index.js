import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import KeyValueView from '../views/KeyValueView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/store', name: 'KeyValue', component: KeyValueView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router