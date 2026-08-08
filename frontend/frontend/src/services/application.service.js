import apiClient from '@/api/apiClient'

class ApplicationService {
  async applyToDrive(driveId) {
    const response = await apiClient.post(`/student/drives/${driveId}/apply`)

    return response.data
  }
  async getStudentApplications() {
    const response = await apiClient.get('/student/applications')
    return response.data
  }
  async exportStudentApplications() {
    const response = await apiClient.get('/student/applications/export')
    return response.data
  }
  async withdrawApplication(applicationId) {
    await apiClient.delete(`/student/applications/${applicationId}`)
  }
}

export default new ApplicationService()
