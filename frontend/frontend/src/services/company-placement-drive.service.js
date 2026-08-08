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
  async updatePlacementDrive(driveId, request) {
    const response = await apiClient.put(`/company/drives/${driveId}`, request)
    return response.data
  }
  async submitPlacementDrive(driveId) {
    const response = await apiClient.patch(`/company/drives/${driveId}/open`)
    return response.data
  }
  async closePlacementDrive(driveId) {
    const response = await apiClient.patch(`/company/drives/${driveId}/close`)
    return response.data
  }
  async cancelPlacementDrive(driveId) {
    const response = await apiClient.patch(`/company/drives/${driveId}/cancel`)
    return response.data
  }
  async deletePlacementDrive(driveId) {
    await apiClient.delete(`/company/drives/${driveId}`)
  }
}

export default new CompanyPlacementDriveService()
