import apiClient from '@/api/apiClient'

class CompanyPlacementDriveService {
  async getCompanyPlacementDrives(params = {}) {
    const response = await apiClient.get('/company/drives', {
      params,
    })

    return response.data
  }
  async getCompanyPlacementDrive(driveId) {
    const response = await apiClient.get(`/company/drives/${driveId}`)
    return response.data
  }
  async createPlacementDrive(request) {
    const response = await apiClient.post('/company/drives', request)

    return response.data
  }
}

export default new CompanyPlacementDriveService()
