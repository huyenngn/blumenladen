import HomeView from '@/views/HomeView.vue'
import InventoryView from '@/views/InventoryView.vue'
import ReportsView from '@/views/ReportsView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      component: HomeView,
    },
    {
      path: '/inventory',
      name: 'Preisverzeichnis',
      component: InventoryView,
    },
    {
      path: '/reports',
      name: 'Berichte',
      component: ReportsView,
    },
  ],
})

export default router
