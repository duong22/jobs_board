<template>
    <BaseLayout>
        <div class="page-header">
          <h1>Open positions</h1>
          <p>{{ filtered.length }} job{{ filtered.length !== 1 ? 's' : '' }} available</p>
        </div>
  
        <div class="filters">
          <input
            v-model="search"
            class="input"
            placeholder="Search job title..."
          />
          <select v-model="filters.category" class="input">
            <option value="">All categories</option>
            <option  v-for="cat in JOB_CATEGORIES" :key="cat.value"  :value="cat.value">
                    {{ cat.label }}
            </option>
          </select>
          <select v-model="filters.job_type" class="input">
            <option value="">All types</option>
            <option value="full_time">Full-time</option>
            <option value="part_time">Part-time</option>
            <option value="internship">Internship</option>
          </select>
          <button v-if="hasFilters" class="btn-clear" @click="clearFilters">Clear</button>
        </div>
  
        <div v-if="loading" class="state-loading">Loading jobs...</div>
          <div v-else-if="error" class="alert-error">{{ error }}</div>
          <div v-else-if="filtered.length === 0" class="state-empty">
          No jobs found. Try adjusting your filters.
        </div>
  
        <div v-else class="job-list">
          <div
            v-for="job in filtered"
            :key="job.id"
            class="job-card"
            @click="$router.push(`/jobs/${job.id}`)"
          >
            <div class="job-card-top">
              <div>
                <div class="job-title">{{ job.title }}</div>
                <div class="job-company">{{ job.company_name }}</div>
              </div>
              <span class="badge badge-blue">{{ job.job_type_display }}</span>
            </div>
            <div class="job-meta">
              <span class="badge badge-gray">{{ job.location }}</span>
              <span class="badge badge-gray">{{ job.category_display }}</span>
            </div>
            <div class="job-date">Posted {{ formatDate(job.created_at) }}</div>
          </div>
        </div>
    </BaseLayout>
</template>
  
<script setup>
  import { ref, computed, onMounted } from 'vue'
  import BaseLayout from './BaseLayout.vue'
  import { JOB_CATEGORIES } from '@/constants/categories'
  import { jobsService } from '@/services/jobs.service'
    
  const jobs = ref([])
  const loading = ref(true)
  const error = ref(null)
  const search = ref('')
  const filters = ref({ category: '', job_type: '' })
  
  const hasFilters = computed(() =>
    search.value || filters.value.category || filters.value.job_type
  )
  
  const filtered = computed(() => {
    return jobs.value.filter(job => {
      const matchSearch = !search.value ||
        job.title.toLowerCase().includes(search.value.toLowerCase()) ||
        job.company_name.toLowerCase().includes(search.value.toLowerCase())
      const matchCategory = !filters.value.category || job.category === filters.value.category
      const matchType = !filters.value.job_type || job.job_type === filters.value.job_type
      return matchSearch && matchCategory && matchType
    })
  })
  
  function clearFilters() {
    search.value = ''
    filters.value = { category: '', job_type: '' }
  }
  
  function formatDate(dateStr) {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
  }
  
  onMounted(async () => {
    try {
      const res = await jobsService.getAll()
      jobs.value = res.data
    } catch {
      error.value = 'Failed to load jobs. Please try again.'
    } finally {
      loading.value = false
    }
  })
</script>
  
<style scoped>
  .filters { display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
  .input {
    padding: 0.6rem 0.9rem; border: 1.5px solid #ddd; border-radius: 6px;
    font-size: 0.875rem; color: #111; background: #fff; outline: none;
    transition: border-color 0.15s;
  }
  .input:focus { border-color: #111; }
  .filters .input:first-child { flex: 1; min-width: 200px; }
  .btn-clear { padding: 0.6rem 1rem; background: none; border: 1.5px solid #ddd; border-radius: 6px; font-size: 0.875rem; color: #888; cursor: pointer; }
  .btn-clear:hover { border-color: #aaa; color: #555; }
  
  .state { text-align: center; padding: 4rem 2rem; color: #888; font-size: 0.9rem; }
  .error { background: #fff0f0; border: 1px solid #fcc; color: #c00; padding: 0.8rem 1rem; border-radius: 6px; font-size: 0.875rem; }
  
  .job-list { display: flex; flex-direction: column; gap: 0.75rem; }
  .job-card {
    background: #fff; border: 1px solid #e5e5e5; border-radius: 8px;
    padding: 1.2rem 1.4rem; cursor: pointer;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .job-card:hover { border-color: #aaa; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  
  .job-card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
  .job-title { font-size: 0.95rem; font-weight: 600; color: #111; }
  .job-company { font-size: 0.85rem; color: #888; margin-top: 0.15rem; }
  
  .job-meta { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.6rem; }
  .job-date { font-size: 0.78rem; color: #aaa; }
</style>