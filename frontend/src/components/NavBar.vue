<template>
  <nav class="nav">
    <router-link to="/" class="logo">JobBoard</router-link>

    <div class="nav-right">
      <router-link to="/jobs" class="nav-link">Browse jobs</router-link>
      <template v-if="!auth.isLoggedIn">
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="nav-btn">Register</router-link>
      </template>

      <template v-else>
        <router-link v-if="auth.role === 'employer'" to="/dashboard" class="nav-link">
          Dashboard
        </router-link>
        <router-link v-if="auth.role === 'candidate'" to="/applications" class="nav-link">
          My applications
        </router-link>
        <router-link to="/profile" class="nav-link">Profile</router-link>
        <span class="nav-role badge badge-pill" :class="'role-' + auth.role">
          {{ auth.role }}
        </span>
        <button class="nav-logout" @click="logout">Logout</button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/auth.service'
const auth = useAuthStore()
async function logout() {
    try {
      await authService.logout(auth.refresh)
    } catch {
    } finally {
      auth.clearSession()
      router.push('/login')
    }
  }
</script>

<style scoped>
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 60px;
  background: var(--white);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 50;
}
.logo {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--ink);
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.nav-link {
  color: var(--ink-soft);
  font-size: 0.9rem;
  padding: 0.3rem 0.6rem;
  border-radius: var(--radius-sm);
  transition: color 0.15s;
}
.nav-link:hover,
.nav-link.router-link-active {
  color: var(--ink);
}
.nav-btn {
  padding: 0.4rem 1rem;
  background: var(--ink);
  color: var(--white);
  border-radius: var(--radius);
  font-size: 0.9rem;
  transition: background 0.15s;
}
.nav-btn:hover {
  background: #333;
}
.nav-role {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.nav-logout {
  padding: 0.35rem 0.8rem;
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.875rem;
  color: var(--ink-soft);
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}
.nav-logout:hover {
  border-color: #aaa;
  color: var(--ink);
}
</style>