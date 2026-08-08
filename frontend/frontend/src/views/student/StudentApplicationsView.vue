<template>
  <AppLayout>
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">My Applications</h2>
        <button class="btn btn-outline-primary" :disabled="exporting" @click="exportHistory">
          {{ exporting ? 'Preparing export...' : 'Export CSV' }}
        </button>
      </div>

      <div v-if="exportMessage" class="alert alert-success">{{ exportMessage }}</div>
      <button v-if="exportTaskId" class="btn btn-success mb-3" @click="downloadExport">Download CSV</button>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <EmptyState
        v-else-if="applications.length === 0"
        message="You haven't applied to any placement drives yet."
        title="No Applications"
      />

      <div v-else>
        <ApplicationCard
          v-for="application in applications"
          :key="application.id"
          :application="application"
          @view-details="viewApplicationDetails"
        />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import applicationService from '@/services/application.service.js'
import ApplicationCard from '@/components/student/application-card/ApplicationCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useRouter } from 'vue-router'

const applications = ref([])
const loading = ref(true)
const error = ref('')
const exporting = ref(false)
const exportMessage = ref('')
const exportTaskId = ref('')

const loadApplications = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await applicationService.getStudentApplications()

    applications.value = response.items
  } catch (err) {
    console.error('Failed to load applications', err)

    error.value = 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  loadApplications()
})

const router = useRouter()

const viewApplicationDetails = (application) => {
  router.push({
    name: 'student-application-details',
    params: {
      applicationId: application.id,
    },
  })
}

const exportHistory = async () => {
  exporting.value = true
  exportMessage.value = ''
  exportTaskId.value = ''
  try {
    const response = await applicationService.exportStudentApplications()
    exportMessage.value = response.message
    await waitForExport(response.task_id)
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to start the application export.'
  } finally {
    exporting.value = false
  }
}

const waitForExport = async (taskId) => {
  const attempts = 30
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    await new Promise((resolve) => window.setTimeout(resolve, 1000))
    const status = await applicationService.getExportStatus(taskId)
    if (status.status === 'SUCCESS') {
      exportTaskId.value = taskId
      exportMessage.value = 'Your export is ready to download.'
      return
    }
    if (status.status === 'FAILURE') {
      throw new Error(status.message)
    }
  }
  exportMessage.value = 'Your export is still being prepared. Please try again shortly.'
}

const downloadExport = async () => {
  try {
    await applicationService.downloadStudentApplications(exportTaskId.value)
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to download the export.'
  }
}
</script>
