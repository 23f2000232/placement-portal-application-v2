import apiClient from '@/api/apiClient'

class CompanyPlacementDriveService {
  async getPlacementDrives() {
    const response = await apiClient.get('/company/drives')

    return response.data
  }
}

export default new CompanyPlacementDriveService()
