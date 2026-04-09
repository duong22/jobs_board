<template>
    <BaseLayout max-width="440px">
        <div class="card" style="margin-top: 2rem">
        <h1 class="page-title">Login</h1>
        <p class="page-sub">Welcome back</p>
  
        <div v-if="error" class="alert-error">{{ error }}</div>
  
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Your username" @keyup.enter="login" />
        </div>
  
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="••••••••" @keyup.enter="login" />
        </div>
  
        <button class="btn-primary" :disabled="loading" @click="login">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
  
        <p class="switch">No account? <router-link to="/register">Register here</router-link></p>
      </div>
    </BaseLayout>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import BaseLayout from './BaseLayout.vue'
  import { useAuthStore } from '@/stores/auth'
  import { authService } from '@/services/auth.service'
  
  const router = useRouter()
  const auth = useAuthStore()
  
  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  const error = ref(null)
  
  async function login() {
    if (!username.value || !password.value) {
      error.value = 'Please fill in all fields'
      return
    }
  
    loading.value = true
    error.value = null
  
    try {
      const response = await authService.login(username.value, password.value)
        auth.setSession(response.data)
        router.push('/profile')
      //   if (auth.role === 'employer') {
      //   router.push('/dashboard')
      // } else {
      //   router.push('/')
      // }
    } catch (err) {
      if (err.response?.status === 401) {
        error.value = 'Invalid username or password'
      } else {
        error.value = 'Something went wrong. Please try again.'
      }
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .switch { text-align: center; font-size: 0.85rem; color: #888; margin-top: 1.2rem; }
  .switch a { color: #111; font-weight: 500; text-decoration: none; }
  .switch a:hover { text-decoration: underline; }
  </style>
  