<script setup>
import { onMounted, reactive, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import CompanyDriveCard from '@/components/company/drive-card/CompanyDriveCard.vue'
import CompanyPlacementDriveService from '@/services/company-placement-drive.service.js'
import { useRouter } from 'vue-router'
import AppButton from '@/components/common/form/AppButton.vue'

const router = useRouter()
const drives = ref([])
const loading = ref(true)

const error = ref('')

const page = ref(1)

const totalPages = ref(0)

const filters = reactive({
  search: '',
  status: '',
  job_type: '',
  is_remote: '',
  sort_by: '',
  sort_direction: '',
})
const loadPlacementDrives = async () => {
  error.value = ''
  loading.value = true

  try {
    const params = {
      page: page.value,
      ...Object.fromEntries(Object.entries(filters).filter(([, value]) => value !== '')),
    }

    const response = await CompanyPlacementDriveService.getCompanyPlacementDrives(params)

    drives.value = response.items

    totalPages.value = response.total_pages
  } catch (err) {
    console.error('Failed to load placement drives', err)

    error.value = 'Failed to load placement drives.'
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  loadPlacementDrives()
})
const createDrive = async () => {
  await router.push({
    name: 'create-company-drive',
  })
}
const viewDrive = async (drive) => {
  await router.push({
    name: 'company-drive-details',
    params: {
      driveId: drive.id,
    },
  })
}
const editDrive = async (drive) => router.push({ name: 'company-drive-edit', params: { driveId: drive.id } })
const deleteDrive = async (drive) => {
  if (!window.confirm('Delete this draft placement drive?')) return
  try { await CompanyPlacementDriveService.deletePlacementDrive(drive.id); await loadPlacementDrives() }
  catch { error.value = 'Only draft placement drives can be deleted.' }
}
</script>
<template>
  <AppLayout>
    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">My Placement Drives</h2>

        <AppButton :block="false" @click="createDrive"> Create Drive </AppButton>
      </div>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <EmptyState
        v-else-if="drives.length === 0"
        message="You haven't created any placement drives yet."
        title="No Placement Drives"
      />

      <div v-if="!loading && !error && drives.length === 0" class="text-center mt-3">
        <AppButton :block="false" @click="createDrive"> Create Your First Drive </AppButton>
      </div>

      <form class="row g-2 mb-4" @submit.prevent="page = 1; loadPlacementDrives()"><div class="col-md-5"><input v-model.trim="filters.search" class="form-control" placeholder="Search by title or location"></div><div class="col-md-3"><select v-model="filters.status" class="form-select"><option value="">All statuses</option><option value="DRAFT">Draft</option><option value="PENDING">Pending approval</option><option value="OPEN">Open</option><option value="CLOSED">Closed</option><option value="CANCELLED">Cancelled</option><option value="REJECTED">Rejected</option></select></div><div class="col-md-2"><select v-model="filters.job_type" class="form-select"><option value="">All job types</option><option value="FULL_TIME">Full time</option><option value="INTERN">Intern</option><option value="INTERNSHIP_WITH_PPO">Internship + PPO</option></select></div><div class="col-md-2"><button class="btn btn-primary w-100">Search</button></div></form>
      <div v-if="!loading && !error && drives.length > 0">
        <CompanyDriveCard
          v-for="drive in drives"
          :key="drive.id"
          :drive="drive"
          @delete="deleteDrive"
          @edit="editDrive"
          @view="viewDrive"
        />
      </div>
    </div>
  </AppLayout>
</template>
