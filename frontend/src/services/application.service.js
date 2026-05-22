import api from './api'

export const applicationsService = {
  apply(jobId, formData) {
    return api.post(`/api/jobs/${jobId}/apply/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getAll() {
    return api.get('/api/applications/')
  },
  getOne(id) {
    return api.get(`/api/applications/${id}/`)
  },
  updateStatus(id, status) {
    return api.patch(`/api/applications/${id}/status/`, { status })
  },
  downloadCv(id) {
    return api.get(`/api/applications/${id}/cv/`, { responseType: 'blob' })
  },
}