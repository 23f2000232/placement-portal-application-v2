<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import placementDriveService from '@/services/placement-drive.service'
import applicationService from '@/services/application.service'
import { getCurrentUser } from '@/utils/auth'

const loading = ref(true)
const error = ref('')
const drivePage = ref(null)
const applicationPage = ref(null)
const currentUser = getCurrentUser()
const cards = computed(() => [
  { label: 'Available drives', value: drivePage.value?.total_items ?? 0 },
  { label: 'Applications', value: applicationPage.value?.total_items ?? 0 },
  {
    label: 'Active applications',
    value:
      applicationPage.value?.items?.filter(
        (item) => !['REJECTED', 'WITHDRAWN'].includes(item.application_status),
      ).length ?? 0,
  },
])
const upcoming = computed(() => drivePage.value?.items?.[0] ?? null)

onMounted(async () => {
  if (currentUser?.approval_status !== 'APPROVED') {
    loading.value = false
    return
  }
  try {
    ;[drivePage.value, applicationPage.value] = await Promise.all([
      placementDriveService.getStudentPlacementDrives({
        size: 20,
        sort_by: 'application_deadline',
        sort_direction: 'asc',
      }),
      applicationService.getStudentApplications(),
    ])
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load your dashboard.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout
    ><div class="container py-4">
      <h1 class="mb-4">Student Dashboard</h1>
      <LoadingSpinner v-if="loading" />
      <div v-else-if="currentUser?.approval_status !== 'APPROVED'" class="alert alert-info">
        Your account is awaiting administrator approval. Dashboard data will be available once it is
        approved.
      </div>
      <ErrorAlert v-else-if="error" :message="error" />
      <template v-else
        ><div class="row g-3">
          <div v-for="card in cards" :key="card.label" class="col-md-4">
            <div class="card shadow-sm h-100">
              <div class="card-body">
                <p class="text-secondary mb-1">{{ card.label }}</p>
                <p class="display-6 mb-0">{{ card.value }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="upcoming" class="card mt-4">
          <div class="card-body">
            <h5>Next application deadline</h5>
            <p class="mb-0">
              {{ upcoming.company_name }} · {{ upcoming.title }} —
              {{ new Date(upcoming.application_deadline).toLocaleString() }}
            </p>
          </div>
        </div>
        <div class="card mt-4">
          <div class="card-body">
            <h5>Approved placement drives</h5>
            <div v-if="!drivePage?.items?.length" class="text-muted">
              There are no approved placement drives available to you right now.
            </div>
            <div v-for="drive in drivePage?.items" :key="drive.id" class="border-bottom py-2">
              <strong>{{ drive.title }}</strong
              ><span class="text-muted">
                · {{ drive.company_name }} · deadline
                {{ new Date(drive.application_deadline).toLocaleDateString() }}</span
              >
            </div>
          </div>
        </div>
      </template>
    </div></AppLayout
  >
</template>
