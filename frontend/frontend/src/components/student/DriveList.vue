<script setup>
import { onMounted, reactive, ref } from 'vue'
import placementDriveService from '@/services/placement-drive.service.js'
import DriveCard from '@/components/student/DriveCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drives = ref([])
const loading = ref(true)
const error = ref('')
const page = ref(1)
const totalPages = ref(0)
const totalItems = ref(0)
const filters = reactive({ search: '', job_type: '', is_remote: '' })
const loadPlacementDrives = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await placementDriveService.getStudentPlacementDrives({
      page: page.value,
      ...Object.fromEntries(Object.entries(filters).filter(([, value]) => value !== '')),
    })
    drives.value = response.items
    page.value = response.page
    totalPages.value = response.total_pages
    totalItems.value = response.total_items
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
const viewDriveDetails = async (drive) => {
  await router.push({
    name: 'student-drive-details',
    params: {
      driveId: drive.id,
    },
  })
}
const resetFilters = () => {
  filters.search = ''
  filters.job_type = ''
  filters.is_remote = ''
  page.value = 1
  loadPlacementDrives()
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3"><h2 class="mb-0">Available Placement Drives</h2><span class="text-muted">{{ totalItems }} available</span></div>
    <form class="row g-2 mb-4" @submit.prevent="page = 1; loadPlacementDrives()"><div class="col-md-6"><input v-model.trim="filters.search" class="form-control" placeholder="Search by job, company, or location"></div><div class="col-md-2"><select v-model="filters.job_type" class="form-select"><option value="">All job types</option><option value="FULL_TIME">Full time</option><option value="INTERN">Intern</option><option value="INTERNSHIP_WITH_PPO">Internship + PPO</option></select></div><div class="col-md-2"><select v-model="filters.is_remote" class="form-select"><option value="">Any location</option><option value="true">Remote</option><option value="false">On-site</option></select></div><div class="col-md-2 d-flex gap-2"><button class="btn btn-primary">Search</button><button class="btn btn-outline-secondary" type="button" @click="resetFilters">Reset</button></div></form>

    <LoadingSpinner v-if="loading" />

    <ErrorAlert v-else-if="error" :message="error" />

    <EmptyState
      v-else-if="drives.length === 0"
      message="There are currently no placement drives available."
      title="No Placement Drives"
    />

    <div v-else class="d-grid gap-3">
      <DriveCard
        v-for="drive in drives"
        :key="drive.id"
        :drive="drive"
        @view-details="viewDriveDetails"
      />
      <nav v-if="totalPages > 1" class="d-flex justify-content-between align-items-center mt-3"><button class="btn btn-outline-secondary" :disabled="page === 1" @click="page--; loadPlacementDrives()">Previous</button><span>Page {{ page }} of {{ totalPages }}</span><button class="btn btn-outline-secondary" :disabled="page === totalPages" @click="page++; loadPlacementDrives()">Next</button></nav>
    </div>
  </div>
</template>

<style scoped></style>
