<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import adminService from '@/services/admin.service'
import { formatEnum } from '@/utils/formatters'
import DashboardChart from '@/components/common/DashboardChart.vue'

const dashboard = ref(null)
const error = ref('')
const cards = computed(() => [
  { label: 'Students', value: dashboard.value?.students ?? '—' },
  { label: 'Companies', value: dashboard.value?.companies ?? '—' },
  { label: 'Placement drives', value: dashboard.value?.placement_drives ?? '—' },
  { label: 'Applications', value: dashboard.value?.applications ?? '—' },
])
const chartSeries = (values) => {
  const entries = Object.entries(values || {})
  const maximum = Math.max(...entries.map(([, count]) => count), 1)
  return entries.map(([label, count]) => ({ label, count, width: `${(count / maximum) * 100}%` }))
}
const driveStatuses = computed(() => chartSeries(dashboard.value?.drive_statuses))
const accountStatuses = computed(() => chartSeries(dashboard.value?.account_statuses))
const applicationStatuses = computed(() => chartSeries(dashboard.value?.application_statuses))

onMounted(async () => {
  try { dashboard.value = await adminService.getDashboard() }
  catch (err) { error.value = err.response?.data?.message || 'Unable to load dashboard data.' }
})
</script>

<template>
  <AppLayout><div class="container-fluid py-3">
    <h1 class="mb-4">Admin Dashboard</h1>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <template v-else>
      <div class="row g-3"><div v-for="card in cards" :key="card.label" class="col-sm-6 col-xl-3"><div class="card h-100 shadow-sm"><div class="card-body"><p class="text-secondary mb-1">{{ card.label }}</p><p class="display-6 mb-0">{{ card.value }}</p></div></div></div></div>
      <div v-if="dashboard" class="mt-4 alert alert-info mb-0">{{ dashboard.pending_companies }} company registration(s) and {{ dashboard.pending_drives }} placement drive(s) await approval.</div>
      <div v-if="dashboard" class="row g-4 mt-1"><section class="col-lg-4"><DashboardChart title="Placement drives by status" :labels="driveStatuses.map((item) => formatEnum(item.label))" :values="driveStatuses.map((item) => item.count)" /></section><section class="col-lg-4"><DashboardChart title="Applications by status" :labels="applicationStatuses.map((item) => formatEnum(item.label))" :values="applicationStatuses.map((item) => item.count)" /></section><section class="col-lg-4"><DashboardChart title="Accounts by status" :labels="accountStatuses.map((item) => formatEnum(item.label))" :values="accountStatuses.map((item) => item.count)" /></section></div>
    </template>
  </div></AppLayout>
</template>
