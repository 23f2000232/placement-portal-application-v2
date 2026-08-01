<script setup>
import adminService from '@/services/admin.service.js'
import { onMounted, ref } from 'vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import CompanyApprovalCard from '@/components/admin/CompanyApprovalCard.vue'

const companies = ref([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const processingCompanyId = ref(null)
const loadPendingCompanies = async () => {
  error.value = ''
  loading.value = true

  try {
    companies.value = await adminService.getPendingCompanies()
  } catch (err) {
    console.error('Failed to load pending companies', err)

    error.value = 'Failed to load pending companies.'
  } finally {
    loading.value = false
  }
}

onMounted(loadPendingCompanies)
const approveCompany = async (company) => {
  error.value = ''
  success.value = ''
  processingCompanyId.value = company.id

  try {
    await adminService.approveCompany(company.id)

    success.value = 'Company approved successfully.'

    await loadPendingCompanies()
  } catch (err) {
    console.error('Failed to approve company', err)

    error.value = 'Failed to approve company.'
  } finally {
    processingCompanyId.value = null
  }
}
const rejectCompany = async (company) => {
  error.value = ''
  success.value = ''
  processingCompanyId.value = company.id

  try {
    await adminService.rejectCompany(company.id)

    success.value = 'Company rejected successfully.'

    await loadPendingCompanies()
  } catch (err) {
    console.error('Failed to reject company', err)

    error.value = 'Failed to reject company.'
  } finally {
    processingCompanyId.value = null
  }
}
</script>

<template>
  <AppLayout>
    <div class="container py-4">
      <h2 class="mb-4">Pending Company Approvals</h2>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>

      <EmptyState
        v-else-if="companies.length === 0"
        message="There are no companies awaiting approval."
        title="No Pending Companies"
      />

      <div v-else>
        <CompanyApprovalCard
          v-for="company in companies"
          :key="company.id"
          :company="company"
          :processing="processingCompanyId === company.id"
          @approve="approveCompany"
          @reject="rejectCompany"
        />
      </div>
    </div>
  </AppLayout>
</template>

<style scoped></style>
