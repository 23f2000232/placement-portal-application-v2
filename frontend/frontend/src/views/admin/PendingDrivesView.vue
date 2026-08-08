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
const filters = ref({ search: '', status: '', job_type: '' })

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await adminService.getDrives({ page: 1, size: 100, ...filters.value })
    drives.value = response.items
  } catch { error.value = 'Unable to load placement drives.' } finally { loading.value = false }
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
    <h2 class="mb-4">Placement Drive Management</h2>
    <form class="row g-2 mb-4" @submit.prevent="load">
      <div class="col-md-4"><input v-model.trim="filters.search" class="form-control" placeholder="Search title or location" /></div>
      <div class="col-md-3"><select v-model="filters.status" class="form-select"><option value="">All statuses</option><option value="DRAFT">Draft</option><option value="PENDING">Pending</option><option value="OPEN">Open</option><option value="CLOSED">Closed</option><option value="REJECTED">Rejected</option><option value="CANCELLED">Cancelled</option></select></div>
      <div class="col-md-3"><select v-model="filters.job_type" class="form-select"><option value="">All job types</option><option value="FULL_TIME">Full time</option><option value="INTERN">Intern</option><option value="INTERNSHIP_WITH_PPO">Internship with PPO</option></select></div>
      <div class="col-md-2"><button class="btn btn-primary w-100">Search</button></div>
    </form>
    <div v-if="notice" class="alert alert-success">{{ notice }}</div>
    <LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" />
    <EmptyState v-else-if="!drives.length" title="No Placement Drives" message="No placement drives match the selected filters." />
    <div v-else class="row g-3"><div v-for="drive in drives" :key="drive.id" class="col-md-6"><article class="card h-100 shadow-sm"><div class="card-body">
      <div class="d-flex justify-content-between"><h5>{{ drive.title }}</h5><span class="badge bg-secondary">{{ formatEnum(drive.status) }}</span></div>
      <p v-if="drive.company_name" class="text-muted mb-1">{{ drive.company_name }}</p><p class="mb-1">{{ drive.job_location }} · {{ formatEnum(drive.job_type) }}</p><p class="text-muted mb-3">Deadline: {{ new Date(drive.application_deadline).toLocaleString() }}</p>
      <template v-if="drive.status === 'PENDING'"><button class="btn btn-success me-2" :disabled="processingId === drive.id" @click="decide(drive, 'approve')">Approve</button><button class="btn btn-outline-danger" :disabled="processingId === drive.id" @click="decide(drive, 'reject')">Reject</button></template>
    </div></article></div></div>
  </div></AppLayout>
</template>
