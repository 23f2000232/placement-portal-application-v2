import apiClient from '@/api/apiClient'

const cleanParams = (params) => Object.fromEntries(
  Object.entries(params).filter(([, value]) => value !== '' && value !== null && value !== undefined),
)

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
  async closeDrive(driveId) {
    const response = await apiClient.patch(`/admin/drives/${driveId}/close`)
    return response.data
  }
  async cancelDrive(driveId) {
    const response = await apiClient.patch(`/admin/drives/${driveId}/cancel`)
    return response.data
  }
  async getUsers(params = {}) {
    const response = await apiClient.get('/admin/users', { params: cleanParams(params) })
    return response.data
  }
  async getStudents(params = {}) {
    const response = await apiClient.get('/admin/students', { params: cleanParams(params) })
    return response.data
  }
  async getCompanies(params = {}) {
    const response = await apiClient.get('/admin/companies', { params: cleanParams(params) })
    return response.data
  }
  async getDrives(params = {}) {
    const response = await apiClient.get('/admin/drives', { params: cleanParams(params) })
    return response.data
  }
  async getApplications() {
    const response = await apiClient.get('/admin/applications')
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
