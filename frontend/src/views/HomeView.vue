<template>
  `<BaseLayout max-width="1100px">
    <section class="hero">
      <h1>Find your next job</h1>
      <p>Browse open positions, apply easily, and track your applications.</p>
      <div class="hero-actions">
        <router-link to="/jobs" class="btn-primary">Browse jobs</router-link>
        <router-link v-if="!auth.isLoggedIn" to="/register" class="btn-outline">Post a job</router-link>
        <router-link v-if="auth.role === 'employer'" to="/jobs/create" class="btn-outline">Post a job</router-link>
      </div>
    </section>

    <section class="stats">
      <div class="stat"><strong>124</strong><span>Open positions</span></div>
      <div class="stat"><strong>38</strong><span>Companies hiring</span></div>
      <div class="stat"><strong>6</strong><span>Categories</span></div>
    </section>

    <section class="how">
      <h2>How it works</h2>
      <div class="steps">
        <div class="step">
          <div class="step-num">1</div>
          <h3>Create account</h3>
          <p>Sign up as a candidate or employer.</p>
        </div>
        <div class="step">
          <div class="step-num">2</div>
          <h3>Browse & apply</h3>
          <p>Filter jobs by category, location, or type.</p>
        </div>
        <div class="step">
          <div class="step-num">3</div>
          <h3>Track status</h3>
          <p>Follow your applications from your dashboard.</p>
        </div>
      </div>
    </section>
  </BaseLayout>`
</template>

<script setup>
import BaseLayout from './BaseLayout.vue';
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
</script>

<style scoped>
.hero { text-align: center; padding: 5rem 2rem; background: #f9f9f9; }
.hero h1 { font-size: 2.5rem; font-weight: 700; color: #111; margin-bottom: 1rem; }
.hero p  { font-size: 1.1rem; color: #555; margin-bottom: 2rem; }
.hero-actions { display: flex; justify-content: center; gap: 1rem; }

.stats {
  display: flex; justify-content: center; gap: 4rem;
  padding: 2.5rem 2rem; background: #fff;
  border-top: 1px solid #e5e5e5; border-bottom: 1px solid #e5e5e5; text-align: center;
}
.stat strong { display: block; font-size: 2rem; font-weight: 700; color: #111; }
.stat span   { font-size: 0.85rem; color: #888; }

.how { padding: 4rem 2rem; max-width: 900px; margin: 0 auto; text-align: center; }
.how h2 { font-size: 1.8rem; font-weight: 700; color: #111; margin-bottom: 2.5rem; }
.steps { display: flex; gap: 2rem; }
.step {
  flex: 1; padding: 2rem 1.5rem;
  background: #f9f9f9; border: 1px solid #e5e5e5; border-radius: 8px;
}
.step-num {
  width: 40px; height: 40px; background: #111; color: #fff;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-weight: 700; margin: 0 auto 1rem;
}
.step h3 { font-size: 1rem; font-weight: 600; color: #111; margin-bottom: 0.5rem; }
.step p  { font-size: 0.875rem; color: #666; line-height: 1.6; }
</style>
