import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access')
  const user = JSON.parse(localStorage.getItem('user') || 'null')
  const role = user?.role || null

  if (to.meta.guestOnly && isLoggedIn) return next('/')
  if (to.meta.requiresAuth && !isLoggedIn) return next('/login')
  if (to.meta.role && role !== to.meta.role) return next('/')
  next()
})

export default router
