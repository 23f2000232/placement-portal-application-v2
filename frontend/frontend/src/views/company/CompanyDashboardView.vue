<template>
  <AppLayout><div class="container py-4"><h1 class="mb-4">Company Dashboard</h1><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><div v-else class="row g-3"><div v-for="card in cards" :key="card.label" class="col-md-3"><div class="card shadow-sm h-100"><div class="card-body"><p class="text-secondary mb-1">{{ card.label }}</p><p class="display-6 mb-0">{{ card.value }}</p></div></div></div></div></div></AppLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import driveService from '@/services/company-placement-drive.service'
const loading = ref(true); const error = ref(''); const drives = ref([])
const cards = computed(() => [{ label: 'Created drives', value: drives.value.length }, { label: 'Open drives', value: drives.value.filter((drive) => drive.status === 'OPEN').length }, { label: 'Pending approval', value: drives.value.filter((drive) => drive.status === 'PENDING').length }, { label: 'Drafts', value: drives.value.filter((drive) => drive.status === 'DRAFT').length }])
onMounted(async () => { try { const result = await driveService.getCompanyPlacementDrives({ page: 1, size: 100 }); drives.value = result.items } catch { error.value = 'Unable to load your dashboard.' } finally { loading.value = false } })
</script>
