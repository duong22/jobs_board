import api from './api'

export const jobsService = {
  getAll() {
    return api.get('/api/jobs/')
  },
  getOne(id) {
    return api.get(`/api/jobs/${id}/`)
  },
  create(data) {
    return api.post('/api/jobs/', data)
  },

  updateOne(id, data) {
    return api.patch(`/api/jobs/${id}`, data)
  },
  removeOne(id) {
    return api.delete(`/api/jobs/${id}`)
  },
  getMine() {
    return api.get('/api/jobs/me/')
  },
}