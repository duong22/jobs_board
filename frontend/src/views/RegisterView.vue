<template>
    <BaseLayout max-width="440px">
    <div class="card" style="margin-top: 2rem">
        <h1 class="page-title">Create account</h1>
        <p class="page-sub">Join as a candidate or employer</p>
  
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
  
        <div class="form-group">
          <label>I am a...</label>
          <div class="role-picker">
            <div
              class="role-option"
              :class="{ active: form.role === 'candidate' }"
              @click="form.role = 'candidate'"
            >
              <div class="role-icon">🎓</div>
              <div class="role-name">Candidate</div>
              <div class="role-desc">Looking for work</div>
            </div>
            <div
              class="role-option"
              :class="{ active: form.role === 'employer' }"
              @click="form.role = 'employer'"
            >
              <div class="role-icon">🏢</div>
              <div class="role-name">Employer</div>
              <div class="role-desc">Hiring talent</div>
            </div>
          </div>
        </div>
  
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="Choose a username" />
        </div>
  
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" placeholder="you@example.com" />
        </div>
  
        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="Min. 8 characters" />
        </div>
  
        <div class="form-group">
          <label>Confirm password</label>
          <input v-model="form.password2" type="password" placeholder="Repeat password" @keyup.enter="register" />
        </div>
  
        <button class="btn-primary" :disabled="loading" @click="register">
          {{ loading ? 'Creating account...' : 'Create account' }}
        </button>
  
        <p class="switch">Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </BaseLayout>
</template>
  
<script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import BaseLayout from './BaseLayout.vue'
  import { authService } from '@/services/auth.service'
  
  const router = useRouter()
  
  const form = reactive({
    username: '',
    email: '',
    password: '',
    password2: '',
    role: 'candidate'   // default selection
  })
  
  const loading = ref(false)
  const error = ref(null)
  const success = ref(null)
  
  async function register() {
    error.value = null
    success.value = null
  
    if (!form.username || !form.email || !form.password || !form.password2) {
      error.value = 'Please fill in all fields'
      return
    }
    if (form.password !== form.password2) {
      error.value = 'Passwords do not match'
      return
    }
    if (!form.role) {
      error.value = 'Please select a role'
      return
    }
  
    loading.value = true
  
    try {
      await authService.register(
        form.username,
        form.email,
        form.password,
        form.password2,
        form.role
      )
  
      success.value = 'Account created! Redirecting to login...'
      setTimeout(() => router.push('/login'), 1500)
  
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const firstError = Object.values(data)[0]
        error.value = Array.isArray(firstError) ? firstError[0] : firstError
      } else {
        error.value = 'Something went wrong. Please try again.'
      }
    } finally {
      loading.value = false
    }
  }
</script>
  
<style scoped>
  .role-picker { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 0.4rem; }
  .role-option {
    border: 1.5px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    cursor: pointer;
    text-align: center;
    transition: border-color 0.15s, background 0.15s;
  }
  .role-option.active { border-color: #111; background: #f9f9f9; }
  .role-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
  .role-name { font-size: 0.875rem; font-weight: 600; color: #111; }
  .role-desc { font-size: 0.75rem; color: #888; margin-top: 0.15rem; }

  .switch { text-align: center; font-size: 0.85rem; color: #888; margin-top: 1.2rem; }
  .switch a { color: #111; font-weight: 500; text-decoration: none; }
  .switch a:hover { text-decoration: underline; }
</style>
  