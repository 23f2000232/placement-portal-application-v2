<template>
  <AppLayout><div class="container py-4"><h1 class="mb-4">Student Dashboard</h1><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><div v-else class="row g-3"><div v-for="card in cards" :key="card.label" class="col-md-4"><div class="card shadow-sm h-100"><div class="card-body"><p class="text-secondary mb-1">{{ card.label }}</p><p class="display-6 mb-0">{{ card.value }}</p></div></div></div></div><div v-if="upcoming" class="card mt-4"><div class="card-body"><h5>Next application deadline</h5><p class="mb-0">{{ upcoming.company_name }} · {{ upcoming.title }} — {{ new Date(upcoming.application_deadline).toLocaleString() }}</p></div></div></div></AppLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import placementDriveService from '@/services/placement-drive.service'
import applicationService from '@/services/application.service'
const loading = ref(true); const error = ref(''); const drivePage = ref(null); const applicationPage = ref(null)
const cards = computed(() => [{ label: 'Available drives', value: drivePage.value?.total_items ?? 0 }, { label: 'Applications', value: applicationPage.value?.total_items ?? 0 }, { label: 'Active applications', value: applicationPage.value?.items?.filter((item) => !['REJECTED', 'WITHDRAWN'].includes(item.application_status)).length ?? 0 }])
const upcoming = computed(() => drivePage.value?.items?.[0] ?? null)
onMounted(async () => { try { [drivePage.value, applicationPage.value] = await Promise.all([placementDriveService.getStudentPlacementDrives({ size: 20, sort_by: 'application_deadline', sort_direction: 'ASC' }), applicationService.getStudentApplications()]) } catch { error.value = 'Unable to load your dashboard.' } finally { loading.value = false } })
</script>
