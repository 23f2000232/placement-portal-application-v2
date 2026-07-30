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
      <ErrorAlert v-if="applyError" :message="applyError" />

      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>
      <DriveApplySection
        :applied="applied"
        :drive="drive"
        :loading="applying"
        @apply="applyToDrive"
      />
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '@/layouts/AppLayout.vue'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import placementDriveService from '@/services/placement-drive.service.js'
import DriveApplySection from '@/components/student/drive-details/DriveApplySection.vue'
import DriveHiringProcess from '@/components/student/drive-details/DriveHiringProcess.vue'
import DriveEligibility from '@/components/student/drive-details/DriveEligibility.vue'
import DriveJobDetails from '@/components/student/drive-details/DriveJobDetails.vue'
import DriveDescription from '@/components/student/drive-details/DriveDescription.vue'
import DriveDetailsHeader from '@/components/student/drive-details/DriveDetailsHeader.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import applicationService from '@/services/application.service.js'

const route = useRoute()

const drive = ref(null)
const loading = ref(true)
const error = ref('')
const applying = ref(false)
const applied = ref(false)
const success = ref('')
const applyError = ref('')
const loadPlacementDrive = async () => {
  error.value = ''
  loading.value = true

  try {
    drive.value = await placementDriveService.getStudentPlacementDrive(route.params.driveId)
  } catch (err) {
    console.error('Failed to load placement drive', err)

    error.value = 'Failed to load placement drive.'
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  loadPlacementDrive()
})
const applyToDrive = async () => {
  success.value = ''
  applyError.value = ''
  applying.value = true

  try {
    await applicationService.applyToDrive(drive.value.id)
    success.value = 'Application submitted successfully.'
    applied.value = true
  } catch (err) {
    console.error('Failed to apply for placement drive', err)
    applyError.value = 'Unable to submit application.'
  } finally {
    applying.value = false
  }
}
</script>
