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
  import { useRouter } from 'vue-router'
  import BaseLayout from './BaseLayout.vue'
  import { useAuthStore } from '@/stores/auth'
  import { profileService } from '@/services/profile.service'
  import { authService } from '@/services/auth.service'
  
  const router = useRouter()
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
  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  /* NAV */
  .nav {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 2rem; height: 60px;
    background: #fff; border-bottom: 1px solid #e5e5e5;
  }
  .logo { font-size: 1.2rem; font-weight: 700; color: #111; text-decoration: none; }
  .nav-right { display: flex; align-items: center; gap: 0.5rem; }
  .nav-link { color: #555; text-decoration: none; font-size: 0.9rem; padding: 0.3rem 0.6rem; }
  .nav-link:hover, .nav-link.active { color: #111; }
  .nav-logout {
    padding: 0.35rem 0.8rem; background: none; border: 1px solid #ddd;
    border-radius: 6px; font-size: 0.875rem; color: #555; cursor: pointer;
  }
  .nav-logout:hover { border-color: #aaa; color: #111; }
  
  /* PAGE */
  .page { min-height: 100vh; background: #f9f9f9; }
  .content { max-width: 640px; margin: 0 auto; padding: 2.5rem 2rem; }
  
  /* STATE */
  .state-msg { text-align: center; padding: 4rem; color: #888; font-size: 0.9rem; }
  
  /* PROFILE HEADER */
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
  .role-badge {
    display: inline-block; margin-top: 0.4rem;
    font-size: 0.72rem; font-weight: 600; padding: 0.2rem 0.6rem;
    border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;
  }
  .role-candidate { background: #fde8d8; color: #b94a1a; }
  .role-employer  { background: #d8f0e8; color: #1a7a4a; }
  
  /* CARD */
  .card {
    background: #fff; border: 1px solid #e5e5e5; border-radius: 8px;
    padding: 1.8rem; margin-bottom: 1.2rem;
  }
  .card h2 { font-size: 1rem; font-weight: 600; color: #111; margin-bottom: 1.4rem; }
  
  /* FORM */
  .form-group { margin-bottom: 1.1rem; }
  .form-group label {
    display: block; font-size: 0.85rem; font-weight: 500;
    color: #333; margin-bottom: 0.4rem;
  }
  .form-group input,
  .form-group textarea {
    width: 100%; padding: 0.65rem 0.9rem;
    border: 1.5px solid #ddd; border-radius: 6px;
    font-size: 0.9rem; color: #111;
    font-family: inherit; outline: none;
    transition: border-color 0.15s;
  }
  .form-group input:focus,
  .form-group textarea:focus { border-color: #111; }
  .form-group textarea { resize: vertical; }
  .hint { font-size: 0.78rem; color: #aaa; margin-top: 0.3rem; display: block; }
  
  .form-actions { margin-top: 1.4rem; }
  
  /* BUTTONS */
  .btn-primary {
    padding: 0.65rem 1.5rem; background: #111; color: #fff;
    border: none; border-radius: 6px; font-size: 0.9rem;
    font-weight: 500; cursor: pointer; transition: background 0.15s;
  }
  .btn-primary:hover:not(:disabled) { background: #333; }
  .btn-primary:disabled { background: #999; cursor: not-allowed; }
  
  .btn-outline {
    padding: 0.65rem 1.5rem; background: #fff; color: #111;
    border: 1.5px solid #ccc; border-radius: 6px; font-size: 0.9rem;
    font-weight: 500; cursor: pointer; transition: border-color 0.15s;
  }
  .btn-outline:hover:not(:disabled) { border-color: #111; }
  .btn-outline:disabled { color: #999; border-color: #ddd; cursor: not-allowed; }
  
  /* FEEDBACK */
  .success {
    background: #f0fff4; border: 1px solid #9be9a8; color: #1a7a4a;
    padding: 0.7rem 0.9rem; border-radius: 6px;
    font-size: 0.875rem; margin-bottom: 1.2rem;
  }
  .error {
    background: #fff0f0; border: 1px solid #fcc; color: #c00;
    padding: 0.7rem 0.9rem; border-radius: 6px;
    font-size: 0.875rem; margin-bottom: 1.2rem;
  }
  </style>