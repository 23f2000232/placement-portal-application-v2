<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import resumeService from '@/services/resume.service'
import apiClient from '@/api/apiClient'
import { getCurrentUser, saveCurrentUser } from '@/utils/auth'

const resume = ref(null)
const file = ref(null)
const loading = ref(true)
const uploading = ref(false)
const deleting = ref(false)
const error = ref('')
const success = ref('')
const profile = ref(null)
const profileSaving = ref(false)

const loadResume = async () => {
  loading.value = true
  error.value = ''
  try { resume.value = await resumeService.getResume() } catch (err) {
    if (err.response?.status !== 404) error.value = err.response?.data?.message || 'Unable to load your resume.'
  } finally { loading.value = false }
}
const chooseFile = (event) => { file.value = event.target.files?.[0] || null; error.value = '' }
const upload = async () => {
  if (!file.value) { error.value = 'Choose a PDF resume before uploading.'; return }
  if (file.value.type && file.value.type !== 'application/pdf') { error.value = 'Only PDF files are allowed.'; return }
  uploading.value = true; error.value = ''; success.value = ''
  try { resume.value = await resumeService.uploadResume(file.value); success.value = 'Resume uploaded successfully.'; file.value = null }
  catch (err) { error.value = err.response?.data?.message || 'Unable to upload your resume.' }
  finally { uploading.value = false }
}
const remove = async () => {
  deleting.value = true; error.value = ''; success.value = ''
  try { await resumeService.deleteResume(); resume.value = null; success.value = 'Resume removed successfully.' }
  catch (err) { error.value = err.response?.data?.message || 'Unable to remove your resume.' }
  finally { deleting.value = false }
}
onMounted(loadResume)
profile.value = getCurrentUser()
const saveProfile = async () => {
  profileSaving.value = true; error.value = ''; success.value = ''
  try {
    const response = await apiClient.put('/student/profile', {
      full_name: profile.value.full_name,
      phone_number: profile.value.phone_number,
      branch: profile.value.branch,
      semester: Number(profile.value.semester),
      cgpa: Number(profile.value.cgpa),
      current_backlogs: Number(profile.value.current_backlogs || 0),
      skills: (profile.value.skills || []).map((skill) => skill.trim()).filter(Boolean),
    })
    profile.value = response.data; saveCurrentUser(response.data); success.value = 'Profile updated successfully.'
  } catch (err) { error.value = err.response?.data?.message || 'Unable to update your profile.' } finally { profileSaving.value = false }
}
</script>

<template>
  <AppLayout><div class="container py-4">
    <h1 class="mb-4">Resume</h1>
    <LoadingSpinner v-if="loading" />
    <template v-else>
      <div v-if="success" class="alert alert-success">{{ success }}</div><ErrorAlert v-if="error" :message="error" />
      <div class="card shadow-sm"><div class="card-body">
        <h5>{{ resume ? 'Replace your resume' : 'Upload your resume' }}</h5>
        <p class="text-muted">Upload a PDF file. It will be used when you apply for placement drives.</p>
        <p v-if="resume" class="mb-3">A resume is currently uploaded (last updated {{ new Date(resume.uploaded_at).toLocaleString() }}).</p>
        <input class="form-control mb-3" type="file" accept="application/pdf,.pdf" @change="chooseFile" />
        <button class="btn btn-primary me-2" :disabled="uploading" @click="upload">{{ uploading ? 'Uploading...' : (resume ? 'Replace resume' : 'Upload resume') }}</button>
        <button v-if="resume" class="btn btn-outline-danger" :disabled="deleting" @click="remove">{{ deleting ? 'Removing...' : 'Remove resume' }}</button>
      </div></div>
      <form v-if="profile" class="card shadow-sm mt-4" @submit.prevent="saveProfile"><div class="card-body"><h5>Profile and skills</h5><div class="row g-3"><div class="col-md-6"><label class="form-label">Full name</label><input v-model.trim="profile.full_name" required class="form-control" /></div><div class="col-md-6"><label class="form-label">Phone number</label><input v-model.trim="profile.phone_number" required class="form-control" /></div><div class="col-md-4"><label class="form-label">Branch</label><input v-model.trim="profile.branch" required class="form-control" /></div><div class="col-md-4"><label class="form-label">Semester</label><input v-model.number="profile.semester" min="1" max="8" required type="number" class="form-control" /></div><div class="col-md-4"><label class="form-label">CGPA</label><input v-model.number="profile.cgpa" min="0" max="10" step="0.01" required type="number" class="form-control" /></div><div class="col-md-6"><label class="form-label">Current backlogs</label><input v-model.number="profile.current_backlogs" min="0" type="number" class="form-control" /></div><div class="col-md-6"><label class="form-label">Skills (comma separated)</label><input :value="(profile.skills || []).join(', ')" class="form-control" placeholder="Python, SQL, Vue" @input="profile.skills = $event.target.value.split(',')" /></div></div><button class="btn btn-primary mt-3" :disabled="profileSaving">{{ profileSaving ? 'Saving...' : 'Save profile' }}</button></div></form>
    </template>
  </div></AppLayout>
</template>
