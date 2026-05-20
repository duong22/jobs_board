import api from './api'

export const applicationsService = {
  apply(jobId, coverLetter = '') {
    return api.post(`/api/jobs/${jobId}/apply/`, { cover_letter: coverLetter })
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
}