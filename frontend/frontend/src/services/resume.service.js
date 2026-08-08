import apiClient from '@/api/apiClient'

class ResumeService {
  async getResume() {
    const response = await apiClient.get('/student/resume')
    return response.data
  }

  async uploadResume(file) {
    const formData = new FormData()
    formData.append('resume', file)
    const response = await apiClient.post('/student/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async deleteResume() {
    await apiClient.delete('/student/resume')
  }
}

export default new ResumeService()
