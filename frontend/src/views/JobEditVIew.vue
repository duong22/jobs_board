<template>
    <BaseLayout max-width="680px">
        <router-link to="/dashboard" class="back-link">← Back to dashboard</router-link>
        <div v-if="loading" class="state-loading">Loading job...</div>
        <div v-else-if="fetchError" class="alert-error">{{ fetchError }}</div>
  
        <template v-else>
          <h1 class="page-title">Edit job</h1>
          <p class="page-sub">Update the details for this position.</p>
  
          <div v-if="error" class="alert-error">{{ error }}</div>
          <div v-if="saveSuccess" class="alert-success">Job updated successfully.</div>
  
          <div class="card">
            <div class="form-group">
              <label>Job title <span class="fomr-req">*</span></label>
              <input v-model="form.title" type="text" />
            </div>
  
            <div class="form-row">
              <div class="form-group">
                <label>Job type <span class="form-req">*</span></label>
                <select v-model="form.job_type">
                  <option value="full_time">Full-time</option>
                  <option value="part_time">Part-time</option>
                  <option value="internship">Internship</option>
                </select>
              </div>
              <div class="form-group">
                <label>Category <span class="form-req">*</span></label>
                <select v-model="form.category">
                    <option  v-for="cat in JOB_CATEGORIES" :key="cat.value"  :value="cat.value">
                    {{ cat.label }}
                </option>
                </select>
              </div>
            </div>
  
            <div class="form-group">
              <label>Location <span class="form-req">*</span></label>
              <input v-model="form.location" type="text" />
            </div>
  
            <div class="form-group">
              <label>Description <span class="fomr-req">*</span></label>
              <textarea v-model="form.description" rows="6" />
            </div>
  
            <div class="form-group">
              <label>Status</label>
              <select v-model="form.status">
                <option value="open">Open</option>
                <option value="closed">Closed</option>
              </select>
              <span class="hint">Set to Closed to hide this job from the public listing.</span>
            </div>
  
            <div class="form-actions">
              <button class="btn-primary" :disabled="saving" @click="save">
                {{ saving ? 'Saving...' : 'Save changes' }}
              </button>
              <router-link to="/dashboard" class="btn-outline">Cancel</router-link>
            </div>
          </div>
        </template>
    </BaseLayout>
  </template>
  
<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import BaseLayout from './BaseLayout.vue'
  import { JOB_CATEGORIES } from '@/constants/categories'
  import { jobsService } from '@/services/jobs.service'
  
  const route = useRoute()
  const loading = ref(true)
  const fetchError = ref(null)
  const saving = ref(false)
  const error = ref(null)
  const saveSuccess = ref(false)
  const form = reactive({
    title: '',
    job_type: '',
    category: '',
    location: '',
    description: '',
    status: 'open',
  })
  
  onMounted(async () => {
    try {
      const res = await jobsService.getOne(route.params.id)
      const j = res.data
      form.title = j.title
      form.job_type = j.job_type
      form.category = j.category
      form.location = j.location
      form.description = j.description
      form.status = j.status
    } catch {
      fetchError.value = 'Failed to load job. It may not exist or you may not have permission.'
    } finally {
      loading.value = false
    }
  })
  
  async function save() {
    error.value = null
    saveSuccess.value = false
  
    if (!form.title || !form.job_type || !form.category || !form.location || !form.description) {
      error.value = 'Please fill in all required fields.'
      return
    }
  
    saving.value = true
    try {
      await jobsService.updateOne(route.params.id, form)
      saveSuccess.value = true
      setTimeout(() => saveSuccess.value = false, 3000)
    } catch (err) {
      const data = err.response?.data
      if (err.response?.status === 403) {
        error.value = 'You do not have permission to edit this job.'
      } else if (data) {
        const first = Object.values(data)[0]
        error.value = Array.isArray(first) ? first[0] : first
      } else {
        error.value = 'Failed to save. Please try again.'
      }
    } finally {
      saving.value = false
    }
  }
</script>
