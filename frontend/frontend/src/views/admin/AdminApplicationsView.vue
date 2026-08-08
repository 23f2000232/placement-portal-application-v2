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
onMounted(async () => { try { applications.value = await adminService.getApplications() } catch { error.value = 'Unable to load applications.' } finally { loading.value = false } })
</script>

<template><AppLayout><div class="container py-4"><h2 class="mb-4">All Student Applications</h2><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!applications.length" title="No Applications" message="No student applications have been submitted." /><div v-else class="table-responsive"><table class="table"><thead><tr><th>Student</th><th>Company</th><th>Drive</th><th>Status</th><th>Applied</th></tr></thead><tbody><tr v-for="application in applications" :key="application.id"><td>{{ application.student_name }}<br><small class="text-muted">{{ application.roll_number }}</small></td><td>{{ application.company_name }}</td><td>{{ application.job_title }}</td><td>{{ formatEnum(application.status) }}</td><td>{{ new Date(application.applied_at).toLocaleString() }}</td></tr></tbody></table></div></div></AppLayout></template>
