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
//
// const editDrive = async (drive) => {}
//
// const deleteDrive = async (drive) => {}
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

      <div v-else>
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
