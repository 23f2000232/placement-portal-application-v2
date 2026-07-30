<script setup>
import { onMounted, ref } from 'vue'
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
const loadPlacementDrives = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await placementDriveService.getStudentPlacementDrives()
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
</script>

<template>
  <div>
    <h2 class="mb-4">Available Placement Drives</h2>

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
    </div>
  </div>
</template>

<style scoped></style>
