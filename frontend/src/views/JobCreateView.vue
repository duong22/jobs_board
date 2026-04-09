<template>
    <BaseLayout max-width="680px">
        <router-link to="/dashboard" class="back-link">← Back to dashboard</router-link>
        <h1 class="page-title">Post a job</h1>
        <p class="page-sub">Fill in the details below to publish a new position.</p>
  
        <div v-if="error" class="alert-error">{{ error }}</div>
  
        <div class="card">
          <div class="form-group">
            <label>Job title <span class="form-req">*</span></label>
            <input v-model="form.title" type="text" placeholder="e.g. Frontend Developer" />
          </div>
  
          <div class="form-row">
            <div class="form-group">
              <label>Job type <span class="fomr-req">*</span></label>
              <select v-model="form.job_type">
                <option value="">Select type</option>
                <option value="full_time">Full-time</option>
                <option value="part_time">Part-time</option>
                <option value="internship">Internship</option>
              </select>
            </div>
            <div class="form-group">
              <label>Category <span class="form-req">*</span></label>
              <select v-model="form.category">
                <option value="">Select category</option>
                <option  v-for="cat in JOB_CATEGORIES" :key="cat.value"  :value="cat.value">
                    {{ cat.label }}
                </option>
              </select>
            </div>
          </div>
  
          <div class="form-group">
            <label>Location <span class="form-req">*</span></label>
            <input v-model="form.location" type="text" placeholder="e.g. Amsterdam, NL or Remote" />
          </div>
  
          <div class="form-group">
            <label>Description <span class="form-req">*</span></label>
            <textarea
              v-model="form.description"
              rows="6"
              placeholder="Describe the role, responsibilities, and requirements..."
            />
          </div>
  
          <div class="form-actions">
            <button class="btn-primary" :disabled="saving" @click="submit">
              {{ saving ? 'Publishing...' : 'Publish job' }}
            </button>
            <router-link to="/dashboard" class="btn-outline">Cancel</router-link>
          </div>
        </div>
    </BaseLayout>
  </template>
  
<script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { JOB_CATEGORIES } from '@/constants/categories'
  import BaseLayout from './BaseLayout.vue'
  import { jobsService } from '@/services/jobs.service'
  
  const router = useRouter()
  const form = reactive({
    title: '',
    job_type: '',
    category: '',
    location: '',
    description: '',
  })
  
  const saving = ref(false)
  const error = ref(null)
  
  async function submit() {
    error.value = null  
    if (!form.title || !form.job_type || !form.category || !form.location || !form.description) {
      error.value = 'Please fill in all required fields.'
      return
    }
    saving.value = true
    try {
      await jobsService.create(form)
      router.push('/dashboard')
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const first = Object.values(data)[0]
        error.value = Array.isArray(first) ? first[0] : first
      } else {
        error.value = 'Failed to create job. Please try again.'
      }
    } finally {
      saving.value = false
    }
  }
</script>
