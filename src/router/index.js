import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AIView from '@/views/AIView.vue';
import AccountView from '@/views/AccountView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/ai',
    name: 'ai',
    component: AIView
  },
  {
    path: '/account',
    name: 'account',
    component: AccountView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
