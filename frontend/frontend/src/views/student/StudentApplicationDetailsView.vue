<template>
  <AppLayout>
    <div class="container py-4"><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><div v-else-if="application" class="card shadow-sm"><div class="card-body"><div class="d-flex justify-content-between"><h2>{{ application.job_title }}</h2><span class="badge bg-primary">{{ formatEnum(application.application_status) }}</span></div><p class="mb-1"><strong>{{ application.company_name }}</strong> · {{ application.job_location }}</p><p>Applied: {{ new Date(application.applied_at).toLocaleString() }}</p><button v-if="application.application_status === 'APPLIED'" class="btn btn-outline-danger" @click="withdraw">Withdraw application</button></div></div></div>
  </AppLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import applicationService from '@/services/application.service'
import { formatEnum } from '@/utils/formatters'
const route = useRoute(); const router = useRouter(); const application = ref(null); const loading = ref(true); const error = ref('')
onMounted(async () => { try { const response = await applicationService.getStudentApplications(); application.value = response.items.find((item) => item.id === route.params.applicationId); if (!application.value) error.value = 'Application not found.' } catch { error.value = 'Unable to load application details.' } finally { loading.value = false } })
const withdraw = async () => { try { await applicationService.withdrawApplication(application.value.id); await router.push({ name: 'student-applications' }) } catch { error.value = 'Unable to withdraw application.' } }
</script>
