<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import adminService from '@/services/admin.service'
import { formatEnum } from '@/utils/formatters'

const applications = ref([])
const loading = ref(true)
const error = ref('')
const filters = ref({ drive: '', company: '', student: '', status: '' })
onMounted(async () => { try { applications.value = await adminService.getApplications() } catch { error.value = 'Unable to load applications.' } finally { loading.value = false } })
</script>

<template><AppLayout><div class="container py-4"><h2 class="mb-4">All Student Applications</h2><form class="row g-2 mb-4" @submit.prevent><div class="col-md-3"><input v-model.trim="filters.drive" class="form-control" placeholder="Search drive"></div><div class="col-md-3"><input v-model.trim="filters.company" class="form-control" placeholder="Search company"></div><div class="col-md-3"><input v-model.trim="filters.student" class="form-control" placeholder="Search student or roll no."></div><div class="col-md-3"><select v-model="filters.status" class="form-select"><option value="">All statuses</option><option value="APPLIED">Applied</option><option value="UNDER_REVIEW">Under review</option><option value="SHORTLISTED">Shortlisted</option><option value="INTERVIEW_SCHEDULED">Interview scheduled</option><option value="SELECTED">Selected</option><option value="REJECTED">Rejected</option><option value="WITHDRAWN">Withdrawn</option></select></div></form><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!applications.length" title="No Applications" message="No student applications have been submitted." /><div v-else class="table-responsive"><table class="table"><thead><tr><th>Student</th><th>Company</th><th>Drive</th><th>Status</th><th>Applied</th></tr></thead><tbody><tr v-for="application in applications" :key="application.id" v-show="(!filters.drive || application.job_title.toLowerCase().includes(filters.drive.toLowerCase())) && (!filters.company || application.company_name.toLowerCase().includes(filters.company.toLowerCase())) && (!filters.student || application.student_name.toLowerCase().includes(filters.student.toLowerCase()) || application.roll_number.toLowerCase().includes(filters.student.toLowerCase())) && (!filters.status || application.status === filters.status)"><td>{{ application.student_name }}<br><small class="text-muted">{{ application.roll_number }}</small></td><td>{{ application.company_name }}</td><td>{{ application.job_title }}</td><td>{{ formatEnum(application.status) }}</td><td>{{ new Date(application.applied_at).toLocaleString() }}</td></tr></tbody></table></div></div></AppLayout></template>
