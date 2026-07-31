<template>
  <AppLayout>
    <LoadingSpinner v-if="loading" />

    <ErrorAlert v-else-if="error" :message="error" />

    <EmptyState
      v-else-if="drives.length === 0"
      message="You haven't created any placement drives yet."
      title="No Placement Drives"
    />

    <div v-else>
      <CompanyDriveCard
        v-for="drive in drives"
        :key="drive.id"
        :drive="drive"
        @edit="editDrive"
        @view="viewDrive"
      />
    </div>
  </AppLayout>
</template>

<script setup>
import companyPlacementDriveService from '@/services/company-placement-drive.service.js'
import { onMounted, ref } from 'vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import CompanyDriveCard from '@/components/company/drive-card/CompanyDriveCard.vue'

const drives = ref([])

const loading = ref(true)

const error = ref('')
const loadPlacementDrives = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await companyPlacementDriveService.getPlacementDrives()

    drives.value = response.items
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
const viewDrive = (drive) => {
  console.log('View drive', drive)
}

const editDrive = (drive) => {
  console.log('Edit drive', drive)
}
</script>
