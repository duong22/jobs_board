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
              <div v-else class="apply-form">
                <textarea v-model="coverLetter" placeholder="Cover letter (optional)" class="form-control mb-1"></textarea>
                <div class="mb-1">
                  <label for="cvFile" style="font-size:0.9rem; font-weight:600; display:block; margin-bottom:0.2rem">Attach CV (PDF, DOCX)</label>
                  <input id="cvFile" type="file" @change="handleFileChange" accept=".pdf,.doc,.docx" class="form-control" />
                </div>
                <button
                  class="btn-primary"
                  :disabled="applying"
                  @click="apply"
                  style="margin-top: 1rem;"
                >
                  {{ applying ? 'Submitting...' : 'Apply now' }}
                </button>
              </div>
            </div>
  
            <div v-else-if="auth.role === 'employer'">
              <router-link :to="`/jobs/${job.id}/edit`" class="btn-outline">
                Edit this job
              </router-link>

              <div class="employer-applications" style="margin-top: 3rem;">
                <h3>Applications for this job</h3>
                <div v-if="applications.length === 0" style="color: #666; margin-top: 1rem;">No applications yet.</div>
                <div v-else class="table-wrap" style="margin-top: 1rem;">
                  <table class="table">
                    <thead>
                      <tr>
                        <th>Candidate</th>
                        <th>Applied</th>
                        <th>Status</th>
                        <th>CV</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="app in applications" :key="app.id">
                        <td>{{ app.candidate_username }}</td>
                        <td>{{ formatDate(app.created_at) }}</td>
                        <td>
                          <select :value="app.status" @change="updateStatus(app.id, $event.target.value)" style="padding: 0.2rem; font-size: 0.85rem; border: 1px solid #ccc; border-radius: 4px;">
                            <option value="pending">Pending</option>
                            <option value="reviewed">Reviewed</option>
                            <option value="accepted">Accepted</option>
                            <option value="rejected">Rejected</option>
                          </select>
                        </td>
                        <td>
                          <button v-if="app.cv_file" @click="downloadCv(app.id)" class="action-link" style="color: #0066cc; border:none; background:none; cursor:pointer;">Download CV</button>
                          <span v-else style="color: #999; font-size: 0.85rem;">No CV</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
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
  import { applicationsService } from '@/services/application.service'
  
  const route = useRoute()
  const auth = useAuthStore()
  
  const job = ref(null)
  const applications = ref([])
  const loading = ref(true)
  const error = ref(null)
  const applying = ref(false)
  const applySuccess = ref(false)
  const applyError = ref(null)
  
  const coverLetter = ref('')
  const cvFile = ref(null)

  function handleFileChange(event) {
    cvFile.value = event.target.files[0] || null
  }

  async function downloadCv(appId) {
    try {
      const res = await applicationsService.downloadCv(appId)
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `cv_application_${appId}`)
      document.body.appendChild(link)
      link.click()
      link.parentNode.removeChild(link)
    } catch (e) {
      alert("Failed to download CV.")
    }
  }

  async function updateStatus(appId, newStatus) {
    try {
      await applicationsService.updateStatus(appId, newStatus)
      const app = applications.value.find(a => a.id === appId)
      if (app) app.status = newStatus
    } catch (e) {
      alert("Failed to update status.")
    }
  }
  
  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
  }
  
  onMounted(async () => {
    try {
      const res = await jobsService.getOne(route.params.id)
      job.value = res.data

      if (auth.role === 'employer') {
        const appsRes = await applicationsService.getAll()
        applications.value = appsRes.data.filter(a => a.job === job.value.id)
      }
    } catch {
      error.value = 'Job not found or failed to load.'
    } finally {
      loading.value = false
    }
  })
  
  async function apply() {
    applying.value = true
    applyError.value = null
    try {
      const formData = new FormData()
      if (coverLetter.value) formData.append('cover_letter', coverLetter.value)
      if (cvFile.value) formData.append('cv_file', cvFile.value)

      await applicationsService.apply(job.value.id, formData)
      applySuccess.value = true
    } catch (err) {
      const data = err.response?.data
      applyError.value = Array.isArray(data) ? data[0] : data?.detail || 'Failed to apply. Please try again.'
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
  
  .form-control {
    width: 100%;
    padding: 0.7rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.95rem;
    font-family: inherit;
  }
  .mb-1 { margin-bottom: 1rem; }
  
  .table { width: 100%; border-collapse: collapse; text-align: left; }
  .table th { border-bottom: 2px solid #eee; padding: 0.8rem 0.5rem; color: #555; font-size: 0.85rem; }
  .table td { border-bottom: 1px solid #eee; padding: 0.8rem 0.5rem; vertical-align: middle; }
  
  .action-link:hover { text-decoration: underline; }
</style>