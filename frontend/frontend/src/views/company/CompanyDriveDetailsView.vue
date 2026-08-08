<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
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
        @applications="viewApplications"
        @delete="deleteDrive"
        @edit="editDrive"
      />
    </div>
  </AppLayout>
</template>

<style scoped></style>
