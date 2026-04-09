<template>
    <BaseLayout max-width="640px">
        <h1 class="page-title">Profile</h1>
        <p class="page-sub">Manage your account infomation</p>
        <div v-if="loading" class="state-msg">Loading profile...</div>
        <div v-else-if="fetchError" class="error">{{ fetchError }}</div>
        <template v-else>
          <div class="profile-header card">
            <div class="avatar">{{ auth.username.charAt(0).toUpperCase() }}</div>
            <div>
              <div class="profile-name">{{ auth.username }}</div>
              <div class="profile-email">{{ auth.user?.email }}</div>
              <span class="badge badge-pill" :class="'role-' + auth.role">{{ auth.role }}</span>
            </div>
          </div>
  
          <div v-if="saveSuccess" class="alert-success">Profile updated successfully.</div>
          <div v-if="saveError" class="alert-error">{{ saveError }}</div>
  
          <div v-if="auth.role === 'candidate'" class="card">
            <h2>My profile</h2>
  
            <div class="form-group">
              <label>Resume URL</label>
              <input
                v-model="form.resume_url"
                type="url"
                placeholder="https://drive.google.com/your-resume"
              />
              <span class="form-hint">Link to your CV (Google Drive, Dropbox, etc.)</span>
            </div>
  
            <div class="form-group">
              <label>LinkedIn URL</label>
              <input
                v-model="form.linkedin_url"
                type="url"
                placeholder="https://linkedin.com/in/your-name"
              />
            </div>
  
            <div class="form-actions">
              <button class="btn-primary" :disabled="saving" @click="save">
                {{ saving ? 'Saving...' : 'Save changes' }}
              </button>
            </div>
          </div>
  
          <div v-else-if="auth.role === 'employer'" class="card">
            <h2>Company profile</h2>
  
            <div class="form-group">
              <label>Company name</label>
              <input
                v-model="form.company_name"
                type="text"
                placeholder="Acme Corp"
              />
            </div>
  
            <div class="form-group">
              <label>Company website</label>
              <input
                v-model="form.company_website"
                type="url"
                placeholder="https://yourcompany.com"
              />
            </div>
  
            <div class="form-group">
              <label>Location</label>
              <input
                v-model="form.location"
                type="text"
                placeholder="Amsterdam, NL"
              />
            </div>
  
            <div class="form-group">
              <label>Description</label>
              <textarea
                v-model="form.description"
                placeholder="Tell candidates about your company..."
                rows="4"
              />
            </div>
  
            <div class="form-actions">
              <button class="btn-primary" :disabled="saving" @click="save">
                {{ saving ? 'Saving...' : 'Save changes' }}
              </button>
            </div>
          </div>
  
]          <div class="card">
            <h2>Change password</h2>
  
            <div v-if="pwSuccess" class="alert-success">Password changed successfully.</div>
            <div v-if="pwError" class="alert-error">{{ pwError }}</div>
  
            <div class="form-group">
              <label>Current password</label>
              <input v-model="pw.old_password" type="password" placeholder="••••••••" />
            </div>
            <div class="form-group">
              <label>New password</label>
              <input v-model="pw.password" type="password" placeholder="••••••••" />
            </div>
            <div class="form-group">
              <label>Confirm new password</label>
              <input v-model="pw.password2" type="password" placeholder="••••••••" />
            </div>
  
            <div class="form-actions">
              <button class="btn-outline" :disabled="pwSaving" @click="changePassword">
                {{ pwSaving ? 'Updating...' : 'Update password' }}
              </button>
            </div>
          </div>
  
        </template>
    </BaseLayout>
  </template>
  
<script setup>
  import { ref, reactive, onMounted } from 'vue'
  import BaseLayout from './BaseLayout.vue'
  import { useAuthStore } from '@/stores/auth'
  import { profileService } from '@/services/profile.service'
  import { authService } from '@/services/auth.service'
  
  const auth = useAuthStore()
  
  const loading = ref(true)
  const fetchError = ref(null)
  const saving = ref(false)
  const saveSuccess = ref(false)
  const saveError = ref(null)
  
  const form = reactive({
    resume_url: '',
    linkedin_url: '',
    company_name: '',
    company_website: '',
    description: '',
    location: '',
  })
  
  onMounted(async () => {
    try {
      let response
      if (auth.role === 'candidate') {
        response = await profileService.getCandidate()
      } else {
        response = await profileService.getEmployer()
      }
      Object.assign(form, response.data)
    } catch (err) {
      fetchError.value = 'Failed to load profile. Please refresh.'
    } finally {
      loading.value = false
    }
  })
  
  async function save() {
    saving.value = true
    saveSuccess.value = false
    saveError.value = null
  
    try {
      if (auth.role === 'candidate') {
        await profileService.updateCandidate({
          resume_url: form.resume_url,
          linkedin_url: form.linkedin_url,
        })
      } else {
        await profileService.updateEmployer({
          company_name: form.company_name,
          company_website: form.company_website,
          description: form.description,
          location: form.location,
        })
      }
      saveSuccess.value = true
      setTimeout(() => saveSuccess.value = false, 3000)
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const first = Object.values(data)[0]
        saveError.value = Array.isArray(first) ? first[0] : first
      } else {
        saveError.value = 'Failed to save. Please try again.'
      }
    } finally {
      saving.value = false
    }
  }
  
  // ---- Change password ----
  const pw = reactive({ old_password: '', password: '', password2: '' })
  const pwSaving = ref(false)
  const pwSuccess = ref(false)
  const pwError = ref(null)
  
  async function changePassword() {
    pwError.value = null
    pwSuccess.value = false
  
    if (!pw.old_password || !pw.password || !pw.password2) {
      pwError.value = 'Please fill in all password fields'
      return
    }
    if (pw.password !== pw.password2) {
      pwError.value = 'New passwords do not match'
      return
    }
  
    pwSaving.value = true
    try {
      await authService.changePassword(
        auth.user.id,
        pw.old_password,
        pw.password,
        pw.password2
      )
      pwSuccess.value = true
      pw.old_password = ''
      pw.password = ''
      pw.password2 = ''
      setTimeout(() => pwSuccess.value = false, 3000)
    } catch (err) {
      const data = err.response?.data
      if (data?.old_password) {
        pwError.value = data.old_password[0]
      } else if (data?.password) {
        pwError.value = data.password[0]
      } else {
        pwError.value = 'Failed to update password.'
      }
    } finally {
      pwSaving.value = false
    }
  }
</script>
  
<style scoped>
  .profile-header {
    display: flex; align-items: center; gap: 1rem;
    background: #fff; border: 1px solid #e5e5e5; border-radius: 8px;
    padding: 1.4rem 1.6rem; margin-bottom: 1.2rem;
  }
  .avatar {
    width: 52px; height: 52px; border-radius: 50%;
    background: #111; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; font-weight: 700; flex-shrink: 0;
  }
  .profile-name  { font-size: 1rem; font-weight: 600; color: #111; }
  .profile-email { font-size: 0.85rem; color: #888; margin-top: 0.1rem; }
</style>