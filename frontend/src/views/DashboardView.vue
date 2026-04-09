<template>
    <BaseLayout>
        <div class="page-header">
          <div>
            <h1>Dashboard</h1>
            <p>Manage your job postings</p>
          </div>
          <router-link to="/jobs/create" class="btn-primary">+ Post a job</router-link>
        </div>
  
        <div v-if="loading" class="state-loading">Loading your jobs...</div>
        <div v-else-if="error" class="alert-error">{{ error }}</div>
  
        <template v-else>
          <div v-if="jobs.length === 0" class="state-empty">
            <p>You haven't posted any jobs yet.</p>
            <router-link to="/jobs/create" class="btn-primary" style="display:inline-block; margin-top:1rem">
              Post your first job
            </router-link>
          </div>
  
          <div v-else class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Posted</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="job in jobs" :key="job.id">
                  <td class="td-title">{{ job.title }}</td>
                  <td>{{ job.job_type_display }}</td>
                  <td>{{ job.category_display }}</td>
                  <td>{{ job.location }}</td>
                  <td>
                    <span class="badge badge-pill" :class="job.status === 'open' ? 'badge-green' : 'badge-gray'">
                      {{ job.status_display }}
                    </span>
                  </td>
                  <td class="td-date">{{ formatDate(job.created_at) }}</td>
                  <td class="td-actions">
                    <router-link :to="`/jobs/${job.id}`" class="action-link">View</router-link>
                    <router-link :to="`/jobs/${job.id}/edit`" class="action-link">Edit</router-link>
                    <button class="action-delete" @click="confirmDelete(job)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
  
        <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
          <div class="modal">
            <h3>Delete job?</h3>
            <p>Are you sure you want to delete <strong>{{ deleteTarget.title }}</strong>? This cannot be undone.</p>
            <div class="modal-actions">
              <button class="btn-outline" @click="deleteTarget = null">Cancel</button>
              <button class="btn-danger" :disabled="deleting" @click="deleteJob">
                {{ deleting ? 'Deleting...' : 'Yes, delete' }}
              </button>
            </div>
          </div>
        </div>
    </BaseLayout>
</template>
  
<script setup>
  import { ref, onMounted } from 'vue'
  import BaseLayout from './BaseLayout.vue'
  import { jobsService } from '@/services/jobs.service'
  
  const jobs = ref([])
  const loading = ref(true)
  const error = ref(null)
  const deleteTarget = ref(null)
  const deleting = ref(false)
  
  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
  }
  
  onMounted(async () => {
    try {
      const res = await jobsService.getMine()
      jobs.value = res.data
    } catch {
      error.value = 'Failed to load your jobs.'
    } finally {
      loading.value = false
    }
  })
  
  function confirmDelete(job) {
    deleteTarget.value = job
  }
  
  async function deleteJob() {
    deleting.value = true
    try {
      await jobsService.removeOne(deleteTarget.value.id)
      jobs.value = jobs.value.filter(j => j.id !== deleteTarget.value.id)
      deleteTarget.value = null
    } catch {
      error.value = 'Failed to delete job.'
      deleteTarget.value = null
    } finally {
      deleting.value = false
    }
  }
</script>
  
<style scoped>
  .td-title { font-weight: 500; color: #111; }
  .td-date { color: #aaa; white-space: nowrap; }
  .td-actions { display: flex; gap: 0.5rem; align-items: center; }
  
  .action-link { font-size: 0.8rem; color: #555; text-decoration: none; padding: 0.2rem 0.5rem; border-radius: 4px; }
  .action-link:hover { background: #f0f0f0; color: #111; }
  .action-delete { font-size: 0.8rem; color: #c00; background: none; border: none; cursor: pointer; padding: 0.2rem 0.5rem; border-radius: 4px; }
  .action-delete:hover { background: #fff0f0; }
</style>