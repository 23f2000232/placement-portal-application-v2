import apiClient from '@/api/apiClient'

class PlacementDriveService {
  async getStudentPlacementDrives(page = 1, size = 20) {
    const response = await apiClient.get('/student/drives', {
      params: {
        page,
        size,
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
