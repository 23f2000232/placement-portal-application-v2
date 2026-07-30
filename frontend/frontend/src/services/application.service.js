import apiClient from '@/api/apiClient'

class ApplicationService {
  async applyToDrive(driveId) {
    const response = await apiClient.post(`/student/drives/${driveId}/apply`)

    return response.data
  }
}

export default new ApplicationService()
