<script setup>
import adminService from '@/services/admin.service.js'
import { onMounted, ref } from 'vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'

const companies = ref([])
const loading = ref(true)
const error = ref('')
const success = ref('')
const processingCompanyId = ref(null)
const filters = ref({ search: '', industry: '', approval_status: '' })
const loadPendingCompanies = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await adminService.getCompanies({ page: 1, size: 100, ...filters.value })
    companies.value = response.items
  } catch (err) {
    console.error('Failed to load pending companies', err)

    error.value = 'Failed to load pending companies.'
  } finally {
    loading.value = false
  }
}
const setAccountStatus = async (company, accountStatus) => {
  processingCompanyId.value = company.id
  error.value = ''
  try {
    await adminService.setUserAccountStatus(company.user_id, accountStatus)
    await loadPendingCompanies()
    success.value = 'Company account updated successfully.'
  } catch { error.value = 'Failed to update the company account.' } finally { processingCompanyId.value = null }
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
      <h2 class="mb-4">Company Management</h2>
      <form class="row g-2 mb-4" @submit.prevent="loadPendingCompanies"><div class="col-md-5"><input v-model.trim="filters.search" class="form-control" placeholder="Search company, contact, or email" /></div><div class="col-md-3"><input v-model.trim="filters.industry" class="form-control" placeholder="Filter by industry" /></div><div class="col-md-3"><select v-model="filters.approval_status" class="form-select"><option value="">All approval states</option><option value="PENDING">Pending</option><option value="APPROVED">Approved</option><option value="REJECTED">Rejected</option></select></div><div class="col-md-1"><button class="btn btn-primary w-100">Search</button></div></form>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>

      <EmptyState
        v-else-if="companies.length === 0"
        message="No companies match the selected filters."
        title="No Companies"
      />

      <div v-else class="table-responsive"><table class="table align-middle"><thead><tr><th>Company</th><th>Industry</th><th>Approval</th><th>Account</th><th>Actions</th></tr></thead><tbody><tr v-for="company in companies" :key="company.id"><td><div>{{ company.company_name }}</div><small class="text-muted">{{ company.email }}</small></td><td>{{ company.industry }}</td><td>{{ company.approval_status }}</td><td><select class="form-select form-select-sm" :disabled="processingCompanyId === company.id" :value="company.account_status" @change="setAccountStatus(company, $event.target.value)"><option value="ACTIVE">Active</option><option value="SUSPENDED">Deactivated</option><option value="BLACKLISTED">Blacklisted</option></select></td><td><template v-if="company.approval_status === 'PENDING'"><button class="btn btn-sm btn-success me-2" :disabled="processingCompanyId === company.id" @click="approveCompany(company)">Approve</button><button class="btn btn-sm btn-outline-danger" :disabled="processingCompanyId === company.id" @click="rejectCompany(company)">Reject</button></template></td></tr></tbody></table></div>
    </div>
  </AppLayout>
</template>

<style scoped></style>
