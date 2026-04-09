import api from './api'

export const authService = {
  login(username, password) {
    return api.post('/auth/login/', { username, password })
  },

  register(username, email, password, password2, role) {
    return api.post('/auth/register/', { username, email, password, password2, role })
  },

  logout(refresh) {
    return api.post('/auth/logout/', { refresh })
  },

  changePassword(userId, oldPassword, password, password2) {
    return api.put(`/auth/change_password/${userId}/`, {
      old_password: oldPassword,
      password,
      password2
    })
  }
}
