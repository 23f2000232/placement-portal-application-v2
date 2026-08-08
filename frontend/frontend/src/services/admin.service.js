import apiClient from '@/api/apiClient'

class AdminService {
  async getDashboard() {
    const response = await apiClient.get('/admin/dashboard')
    return response.data
  }
  async getPendingStudents() {
    const response = await apiClient.get('/admin/students/pending')

    return response.data
  }
  async getPendingDrives() {
    const response = await apiClient.get('/admin/drives/pending')
    return response.data
  }
  async approveDrive(driveId) {
    const response = await apiClient.patch(`/admin/drives/${driveId}/approve`)
    return response.data
  }
  async rejectDrive(driveId) {
    const response = await apiClient.patch(`/admin/drives/${driveId}/reject`)
    return response.data
  }
  async getUsers(params = {}) {
    const response = await apiClient.get('/admin/users', { params })
    return response.data
  }
  async setUserAccountStatus(userId, accountStatus) {
    const response = await apiClient.patch(`/admin/users/${userId}/account-status`, {
      account_status: accountStatus,
    })
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
