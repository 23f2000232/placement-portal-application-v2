<script setup>
import { computed, onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import driveService from '@/services/company-placement-drive.service'
import companyService from '@/services/company.service'
import { getCurrentUser } from '@/utils/auth'
import { formatEnum } from '@/utils/formatters'

const loading = ref(true)
const error = ref('')
const drives = ref([])
const applicantCounts = ref({})
const company = getCurrentUser()
const cards = computed(() => [
  { label: 'Created drives', value: drives.value.length },
  { label: 'Open drives', value: drives.value.filter((drive) => drive.status === 'OPEN').length },
  { label: 'Pending approval', value: drives.value.filter((drive) => drive.status === 'PENDING').length },
  { label: 'Total applicants', value: Object.values(applicantCounts.value).reduce((sum, value) => sum + value, 0) },
])
onMounted(async () => {
  try {
    const result = await driveService.getCompanyPlacementDrives({ page: 1, size: 100 })
    drives.value = result.items
    const counts = await Promise.all(drives.value.map(async (drive) => {
      const applications = await companyService.getDriveApplications(drive.id, { page: 1, size: 1 })
      return [drive.id, applications.total_items]
    }))
    applicantCounts.value = Object.fromEntries(counts)
  } catch (err) { error.value = err.response?.data?.message || 'Unable to load your dashboard.' } finally { loading.value = false }
})
</script>

<template>
  <AppLayout><div class="container py-4"><h1 class="mb-4">Company Dashboard</h1><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" />
    <template v-else><div class="row g-3"><div v-for="card in cards" :key="card.label" class="col-md-3"><div class="card shadow-sm h-100"><div class="card-body"><p class="text-secondary mb-1">{{ card.label }}</p><p class="display-6 mb-0">{{ card.value }}</p></div></div></div></div>
      <div class="row g-4 mt-1"><section class="col-lg-4"><div class="card h-100 shadow-sm"><div class="card-body"><h5>{{ company?.company_name }}</h5><p class="mb-1">{{ company?.industry }}</p><p class="mb-1">{{ company?.contact_person }}</p><a v-if="company?.website" :href="company.website" target="_blank" rel="noreferrer">Website</a></div></div></section><section class="col-lg-8"><div class="card h-100 shadow-sm"><div class="card-body"><h5>Applicants by placement drive</h5><div v-if="!drives.length" class="text-muted">Create a placement drive to start receiving applications.</div><div v-for="drive in drives" :key="drive.id" class="d-flex justify-content-between border-bottom py-2"><span>{{ drive.title }} <small class="text-muted">({{ formatEnum(drive.status) }})</small></span><strong>{{ applicantCounts[drive.id] ?? 0 }}</strong></div></div></div></section></div>
    </template>
  </div></AppLayout>
</template>
