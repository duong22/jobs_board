import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const access = ref(localStorage.getItem('access') || null)
  const refresh = ref(localStorage.getItem('refresh') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!access.value)
  const role = computed(() => user.value?.role || null)
  const username = computed(() => user.value?.username || '')
  
  function setSession(data) {
    access.value = data.access
    refresh.value = data.refresh
    user.value = {
      id: data.id,
      username: data.username,
      email: data.email,
      role: data.role
    }
    localStorage.setItem('access', data.access)
    localStorage.setItem('refresh', data.refresh)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  function clearSession() {
    access.value = null
    refresh.value = null
    user.value = null
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    localStorage.removeItem('user')
  }

  return { access, refresh, user, isLoggedIn, role, username, setSession, clearSession }
})
