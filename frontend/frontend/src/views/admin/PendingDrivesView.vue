<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import adminService from '@/services/admin.service'
import { formatEnum } from '@/utils/formatters'

const drives = ref([])
const loading = ref(true)
const error = ref('')
const notice = ref('')
const processingId = ref('')

const load = async () => {
  loading.value = true
  error.value = ''
  try { drives.value = await adminService.getPendingDrives() } catch { error.value = 'Unable to load pending placement drives.' } finally { loading.value = false }
}
const decide = async (drive, action) => {
  processingId.value = drive.id
  error.value = ''
  try {
    await (action === 'approve' ? adminService.approveDrive(drive.id) : adminService.rejectDrive(drive.id))
    notice.value = `Drive ${action}d successfully.`
    await load()
  } catch { error.value = `Unable to ${action} this drive.` } finally { processingId.value = '' }
}
onMounted(load)
</script>

<template>
  <AppLayout><div class="container py-4">
    <h2 class="mb-4">Pending Drive Approvals</h2>
    <div v-if="notice" class="alert alert-success">{{ notice }}</div>
    <LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" />
    <EmptyState v-else-if="!drives.length" title="No Pending Drives" message="There are no placement drives awaiting approval." />
    <div v-else class="row g-3"><div v-for="drive in drives" :key="drive.id" class="col-md-6"><article class="card h-100 shadow-sm"><div class="card-body">
      <div class="d-flex justify-content-between"><h5>{{ drive.title }}</h5><span class="badge bg-warning text-dark">{{ formatEnum(drive.status) }}</span></div>
      <p class="mb-1">{{ drive.job_location }} · {{ drive.job_type }}</p><p class="text-muted mb-3">Deadline: {{ new Date(drive.application_deadline).toLocaleString() }}</p>
      <button class="btn btn-success me-2" :disabled="processingId === drive.id" @click="decide(drive, 'approve')">Approve</button><button class="btn btn-outline-danger" :disabled="processingId === drive.id" @click="decide(drive, 'reject')">Reject</button>
    </div></article></div></div>
  </div></AppLayout>
</template>
