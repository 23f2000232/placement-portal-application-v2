<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import resumeService from '@/services/resume.service'

const resume = ref(null)
const file = ref(null)
const loading = ref(true)
const uploading = ref(false)
const deleting = ref(false)
const error = ref('')
const success = ref('')

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
    </template>
  </div></AppLayout>
</template>
