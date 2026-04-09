import api from './api'

export const profileService = {
  getCandidate() {
    return api.get('/api/profile/candidate/')
  },
  updateCandidate(data) {
    return api.patch('/api/profile/candidate/', data)
  },

  getEmployer() {
    return api.get('/api/profile/employer/')
  },
  updateEmployer(data) {
    return api.patch('/api/profile/employer/', data)
  },
}