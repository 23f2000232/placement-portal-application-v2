<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import companyService from '@/services/company.service'
import { formatEnum } from '@/utils/formatters'
const interviews = ref([]); const loading = ref(true); const error = ref('')
onMounted(async () => { try { interviews.value = await companyService.getStudentInterviews() } catch { error.value = 'Unable to load interviews.' } finally { loading.value = false } })
</script>
<template><AppLayout><div class="container py-4"><h2>My Upcoming Interviews</h2><LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!interviews.length" title="No Interviews" message="You have no upcoming interviews." /><div v-else class="table-responsive"><table class="table"><thead><tr><th>Round</th><th>When</th><th>Mode</th><th>Location / Link</th><th>Status</th></tr></thead><tbody><tr v-for="interview in interviews" :key="interview.id"><td>{{ interview.round_number }}</td><td>{{ new Date(interview.scheduled_for).toLocaleString() }}</td><td>{{ formatEnum(interview.interview_mode) }}</td><td><a v-if="interview.meeting_link" :href="interview.meeting_link" target="_blank" rel="noopener">Join meeting</a><span v-else>{{ interview.location || '—' }}</span></td><td>{{ formatEnum(interview.status) }}</td></tr></tbody></table></div></div></AppLayout></template>
