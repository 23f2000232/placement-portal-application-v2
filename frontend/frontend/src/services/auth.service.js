import apiClient from '@/api/apiClient'

class AuthService {
  async login(loginRequest) {
    const response = await apiClient.post('/auth/login', loginRequest)

    return response.data
  }
  async getCurrentUser() {
    const response = await apiClient.get('/auth/me')

    return response.data
  }
  async registerStudent(request) {
    const response = await apiClient.post('/auth/register/student', request)

    return response.data
  }
  async registerCompany(request) {
    const response = await apiClient.post('/auth/register/company', request)

    return response.data
  }
}

export default new AuthService()
