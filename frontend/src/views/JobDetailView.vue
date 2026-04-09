<template>
    <BaseLayout max-width="720px">
        <router-link to="/jobs" class="back-link">← Back to jobs</router-link>
  
        <div v-if="loading" class="state-loading">Loading...</div>
        <div v-else-if="error" class="alert-error">{{ error }}</div>
  
        <template v-else-if="job">
          <div class="job-header">
            <div>
              <h1 class="page-title">{{ job.title }}</h1>
              <p class="company">{{ job.company_name }} · {{ job.location }}</p>
            </div>
            <span class="badge badge-blue">{{ job.job_type_display }}</span>
          </div>
  
          <div class="tags">
            <span class="badge badge-gray">{{ job.category_display }}</span>
            <span class="badge badge-gray">{{ job.location }}</span>
            <span class="badge badge-gray">Posted {{ formatDate(job.created_at) }}</span>
          </div>
  
          <div class="card">
            <h2>About the role</h2>
            <p class="description">{{ job.description }}</p>
          </div>
  
          <div class="apply-section">
            <div v-if="!auth.isLoggedIn" class="alert-info">
              <router-link to="/login">Login</router-link> or
              <router-link to="/register">register</router-link>
              to apply for this position.
            </div>
  
            <div v-else-if="auth.role === 'candidate'">
              <div v-if="applySuccess" class="alert-success">
                Application submitted successfully!
              </div>
              <div v-else-if="applyError" class="alert-error">{{ applyError }}</div>
              <button
                v-else
                class="btn-primary"
                :disabled="applying"
                @click="apply"
              >
                {{ applying ? 'Submitting...' : 'Apply now' }}
              </button>
            </div>
  
            <div v-else-if="auth.role === 'employer'">
              <router-link :to="`/jobs/${job.id}/edit`" class="btn-outline">
                Edit this job
              </router-link>
            </div>
          </div>
        </template>
    </BaseLayout>
</template>
  
<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import BaseLayout from './BaseLayout.vue'
  import { useAuthStore } from '@/stores/auth'
  import { jobsService } from '@/services/jobs.service'
  
  const route = useRoute()
  const auth = useAuthStore()
  
  const job = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const applying = ref(false)
  const applySuccess = ref(false)
  const applyError = ref(null)
  
  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
  }
  
  onMounted(async () => {
    try {
      const res = await jobsService.getOne(route.params.id)
      job.value = res.data
    } catch {
      error.value = 'Job not found.'
    } finally {
      loading.value = false
    }
  })
  
  async function apply() {
    applying.value = true
    applyError.value = null
    try {
      await new Promise(r => setTimeout(r, 600)) // placeholder
      applySuccess.value = true
    } catch (err) {
      const data = err.response?.data
      applyError.value = data?.detail || 'Failed to apply. Please try again.'
    } finally {
      applying.value = false
    }
  }

</script>
  
<style scoped>
  .job-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    gap: 1rem; margin-bottom: 1rem;
  }
  .company { font-size: 0.9rem; color: #888; margin-top: 0.3rem; }  
  .tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
  .description { font-size: 0.9rem; color: #555; line-height: 1.75; white-space: pre-line; }
</style>