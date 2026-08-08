<template>
  <AppLayout>
    <div class="container-fluid py-3">
      <h1 class="mb-4">Admin Dashboard</h1>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-else class="row g-3">
        <div v-for="card in cards" :key="card.label" class="col-sm-6 col-xl-3">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <p class="text-secondary mb-1">{{ card.label }}</p>
              <p class="display-6 mb-0">{{ card.value }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-if="dashboard" class="mt-4 alert alert-info mb-0">
        {{ dashboard.pending_companies }} company registration(s) and
        {{ dashboard.pending_drives }} placement drive(s) await approval.
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import adminService from '@/services/admin.service'

const dashboard = ref(null)
const error = ref('')
const cards = computed(() => [
  { label: 'Students', value: dashboard.value?.students ?? '—' },
  { label: 'Companies', value: dashboard.value?.companies ?? '—' },
  { label: 'Placement drives', value: dashboard.value?.placement_drives ?? '—' },
  { label: 'Applications', value: dashboard.value?.applications ?? '—' },
])

onMounted(async () => {
  try {
    dashboard.value = await adminService.getDashboard()
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load dashboard data.'
  }
})
</script>
