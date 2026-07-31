<template>
  <AppLayout>
    <div class="container py-4">
      <h2 class="mb-4">My Applications</h2>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <EmptyState
        v-else-if="applications.length === 0"
        message="You haven't applied to any placement drives yet."
        title="No Applications"
      />

      <div v-else>
        <ApplicationCard
          v-for="application in applications"
          :key="application.id"
          :application="application"
          @view-details="viewApplicationDetails"
        />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import applicationService from '@/services/application.service.js'
import ApplicationCard from '@/components/student/application-card/ApplicationCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useRouter } from 'vue-router'

const applications = ref([])
const loading = ref(true)
const error = ref('')

const loadApplications = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await applicationService.getStudentApplications()

    applications.value = response.items
  } catch (err) {
    console.error('Failed to load applications', err)

    error.value = 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}
onMounted(() => {
  loadApplications()
})

const router = useRouter()

const viewApplicationDetails = (application) => {
  router.push({
    name: 'student-application-details',
    params: {
      applicationId: application.id,
    },
  })
}
</script>
