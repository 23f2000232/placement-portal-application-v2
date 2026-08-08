import apiClient from '@/api/apiClient'

class PlacementDriveService {
  async getStudentPlacementDrives(params = {}) {
    const response = await apiClient.get('/student/drives', {
      params: {
        page: 1,
        size: 20,
        ...params,
      },
    })

    return response.data
  }
  async getStudentPlacementDrive(driveId) {
    const response = await apiClient.get(`/student/drives/${driveId}`)

    return response.data
  }
}

export default new PlacementDriveService()
