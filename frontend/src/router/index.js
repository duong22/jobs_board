import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DashboardView from '@/views/DashboardView.vue'
import JobView from '@/views/JobView.vue'
import JobDetailView from '@/views/JobDetailView.vue'
import JobCreateView from '@/views/JobCreateView.vue'
import JobEditVIew from '@/views/JobEditVIew.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  // Add as you build:
  { path: '/jobs', name: 'jobs', component: JobView },
  { path: '/jobs/:id', name: 'jobs-detail', component: JobDetailView},
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
  // { path: '/applications', name: 'applications', component: () => import('@/views/ApplicationsView.vue'), meta: { requiresAuth: true, role: 'candidate' } },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true, role: 'employer' } },
  { path: '/jobs/create', name: 'jobs-create', component: JobCreateView, meta: { requiresAuth: true, role: 'employer' } },
  { path: '/jobs/:id/edit', name: 'jobs-edit', component: JobEditVIew, meta: { requiresAuth: true, role: 'employer' } },
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
