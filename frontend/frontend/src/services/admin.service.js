import apiClient from '@/api/apiClient'

class AdminService {
  async getPendingStudents() {
    const response = await apiClient.get('/admin/students/pending')

    return response.data
  }
  async approveStudent(studentId) {
    const response = await apiClient.patch(`/admin/students/${studentId}/approve`)

    return response.data
  }

  async rejectStudent(studentId) {
    const response = await apiClient.patch(`/admin/students/${studentId}/reject`)

    return response.data
  }
  async getPendingCompanies() {
    const response = await apiClient.get('/admin/companies/pending')

    return response.data
  }

  async approveCompany(companyId) {
    const response = await apiClient.patch(`/admin/companies/${companyId}/approve`)

    return response.data
  }

  async rejectCompany(companyId) {
    const response = await apiClient.patch(`/admin/companies/${companyId}/reject`)

    return response.data
  }
}

export default new AdminService()
