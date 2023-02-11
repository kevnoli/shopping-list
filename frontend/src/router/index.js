// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
      {
        path: 'shopping-lists',
        name: 'shopping-lists',
        component: () => import(/* webpackChunkName: "shopping-lists" */ '@/views/ShoppingLists.vue'),
      },
      {
        path: 'shopping-list/:id',
        name: 'shopping-list-details',
        component: () => import(/* webpackChunkName: "shopping-list-details" */ '@/views/ShoppingListDetails.vue'),
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '@/views/Login.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import(/* webpackChunkName: "not-found" */ '@/views/NotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
