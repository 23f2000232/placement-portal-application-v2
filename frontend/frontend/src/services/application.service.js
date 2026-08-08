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
  async getExportStatus(taskId) {
    const response = await apiClient.get(`/student/applications/export/${taskId}/status`)
    return response.data
  }
  async downloadStudentApplications(taskId) {
    const response = await apiClient.get(`/student/applications/export/${taskId}/download`, {
      responseType: 'blob',
    })
    const url = URL.createObjectURL(new Blob([response.data], { type: 'text/csv' }))
    const link = document.createElement('a')
    link.href = url
    link.download = 'placement-applications.csv'
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }
  async withdrawApplication(applicationId) {
    await apiClient.delete(`/student/applications/${applicationId}`)
  }
}

export default new ApplicationService()
