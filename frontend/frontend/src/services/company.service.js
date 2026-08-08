import apiClient from '@/api/apiClient'

class CompanyService {
  async getDriveApplications(driveId, params = {}) {
    const response = await apiClient.get(`/company/drives/${driveId}/applications`, { params })
    return response.data
  }
  async getApplication(applicationId) {
    const response = await apiClient.get(`/company/applications/${applicationId}`)
    return response.data
  }
  async viewApplicationResume(applicationId) {
    const response = await apiClient.get(`/company/applications/${applicationId}/resume`, { responseType: 'blob' })
    const url = URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
    window.open(url, '_blank', 'noopener,noreferrer')
    window.setTimeout(() => URL.revokeObjectURL(url), 60_000)
  }
  async updateApplicationStatus(applicationId, action) {
    const response = await apiClient.patch(`/company/applications/${applicationId}/${action}`)
    return response.data
  }
  async getCompanyInterviews() {
    const response = await apiClient.get('/company/interviews')
    return response.data
  }
  async getStudentInterviews() {
    const response = await apiClient.get('/student/interviews')
    return response.data
  }
  async createInterview(applicationId, request) {
    const response = await apiClient.post(`/company/applications/${applicationId}/interviews`, request)
    return response.data
  }
  async updateInterview(interviewId, request) {
    const response = await apiClient.patch(`/company/interviews/${interviewId}`, request)
    return response.data
  }
  async completeInterview(interviewId, request) {
    const response = await apiClient.patch(`/company/interviews/${interviewId}/complete`, request)
    return response.data
  }
}

export default new CompanyService()
