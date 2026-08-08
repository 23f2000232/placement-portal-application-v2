<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import companyPlacementDriveService from '@/services/company-placement-drive.service.js'
import DriveHiringProcess from '@/components/student/drive-details/DriveHiringProcess.vue'
import DriveEligibility from '@/components/student/drive-details/DriveEligibility.vue'
import DriveJobDetails from '@/components/student/drive-details/DriveJobDetails.vue'
import DriveDescription from '@/components/student/drive-details/DriveDescription.vue'
import DriveDetailsHeader from '@/components/student/drive-details/DriveDetailsHeader.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import CompanyDriveManagementSection from '@/components/company/CompanyDriveManagementSection.vue'

const route = useRoute()
const router = useRouter()

const drive = ref(null)

const loading = ref(true)

// const editDrive = async () => {}
//
// const deleteDrive = async () => {}
//
// const viewApplications = async () => {}
const error = ref('')
const loadPlacementDrive = async () => {
  error.value = ''
  loading.value = true

  try {
    drive.value = await companyPlacementDriveService.getCompanyPlacementDrive(route.params.driveId)
  } catch (err) {
    console.error(err)

    error.value = 'Failed to load placement drive.'
  } finally {
    loading.value = false
  }
}

onMounted(loadPlacementDrive)
const manage = async (action) => {
  try {
    if (action === 'submit') await companyPlacementDriveService.submitPlacementDrive(drive.value.id)
    if (action === 'close') await companyPlacementDriveService.closePlacementDrive(drive.value.id)
    if (action === 'cancel') await companyPlacementDriveService.cancelPlacementDrive(drive.value.id)
    await loadPlacementDrive()
  } catch {
    error.value = `Unable to ${action} this drive.`
  }
}
const deleteDrive = async () => {
  if (!window.confirm('Delete this draft placement drive?')) return
  try {
    await companyPlacementDriveService.deletePlacementDrive(drive.value.id)
    await router.push({ name: 'company-drives' })
  } catch {
    error.value = 'Unable to delete this drive.'
  }
}
const editDrive = async () => router.push({ name: 'company-drive-edit', params: { driveId: drive.value.id } })
const viewApplications = async () => router.push({ name: 'company-applications' })
</script>

<template>
  <AppLayout>
    <LoadingSpinner v-if="loading" />

    <ErrorAlert v-else-if="error" :message="error" />

    <div v-else class="container py-4">
      <DriveDetailsHeader :drive="drive" />

      <DriveDescription :drive="drive" />

      <DriveJobDetails :drive="drive" />

      <DriveEligibility :drive="drive" />

      <DriveHiringProcess :drive="drive" />

      <CompanyDriveManagementSection
        :drive="drive"
        @edit="editDrive"
        @applications="viewApplications"
        @delete="deleteDrive"
        @submit="manage('submit')"
        @close="manage('close')"
        @cancel="manage('cancel')"
      />
    </div>
  </AppLayout>
</template>

<style scoped></style>
