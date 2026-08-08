<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import companyService from '@/services/company.service'
import { formatEnum } from '@/utils/formatters'
const interviews = ref([]); const loading = ref(true); const error = ref('')
onMounted(async () => { try { interviews.value = await companyService.getStudentInterviews() } catch (err) { error.value = err.response?.data?.message || 'Unable to load interviews.' } finally { loading.value = false } })
</script>
<template><AppLayout><div class="container py-4"><h2>My Interviews</h2><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!interviews.length" title="No Interviews" message="Interview invitations will appear here when a company schedules them." /><div v-else class="table-responsive"><table class="table align-middle"><thead><tr><th>Company / role</th><th>Round</th><th>When</th><th>Mode</th><th>Location / Link</th><th>Status</th></tr></thead><tbody><tr v-for="interview in interviews" :key="interview.id"><td>{{ interview.company_name }}<br><small class="text-muted">{{ interview.job_title }}</small></td><td>{{ interview.round_number }}</td><td>{{ new Date(interview.scheduled_for).toLocaleString() }}</td><td>{{ formatEnum(interview.interview_mode) }}</td><td><a v-if="interview.meeting_link && interview.status === 'SCHEDULED'" :href="interview.meeting_link" target="_blank" rel="noopener">Join meeting</a><span v-else>{{ interview.location || '—' }}</span></td><td>{{ formatEnum(interview.status) }}<br><small v-if="interview.feedback" class="text-muted">{{ interview.feedback }}</small></td></tr></tbody></table></div></div></AppLayout></template>
