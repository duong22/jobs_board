<template>
  <BaseLayout>
    <div class="page-header">
      <h1>My applications</h1>
      <p>Track every position you've applied to</p>
    </div>

    <div v-if="loading" class="state-loading">Loading...</div>
    <div v-else-if="error" class="alert-error">{{ error }}</div>

    <template v-else>
      <div v-if="applications.length === 0" class="state-empty">
        You haven't applied to any jobs yet.
        <router-link to="/jobs" style="display:block; margin-top:1rem" class="btn-primary">
          Browse jobs
        </router-link>
      </div>

      <div v-else class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Company</th>
              <th>Applied</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td class="td-title">
                <router-link :to="`/jobs/${app.job}`">{{ app.job_title }}</router-link>
              </td>
              <td>{{ app.company_name }}</td>
              <td style="color: var(--ink-faint)">{{ formatDate(app.created_at) }}</td>
              <td>
                <span class="badge badge-pill" :class="statusBadge(app.status)">
                  {{ app.status_display }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseLayout from './BaseLayout.vue'
import { applicationsService } from '@/services/application.service'

const applications = ref([])
const loading      = ref(true)
const error        = ref(null)

const statusBadge = (s) => ({
  pending:  'badge-gray',
  reviewed: 'badge-blue',
  accepted: 'badge-green',
  rejected: 'badge-red',
}[s] || 'badge-gray')

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try   { applications.value = (await applicationsService.getAll()).data }
  catch { error.value = 'Failed to load applications.' }
  finally { loading.value = false }
})
</script>

<style scoped>
.td-title a { color: var(--ink); font-weight: 500; }
.td-title a:hover { text-decoration: underline; }
</style>