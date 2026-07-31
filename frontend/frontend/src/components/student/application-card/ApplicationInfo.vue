<script setup>
import { computed } from 'vue'

import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate } from '@/utils/formatters'

const props = defineProps({
  application: {
    type: Object,
    required: true,
  },
})

const formattedAppliedDate = computed(() => formatDate(props.application.applied_at))
</script>

<template>
  <div class="card-body">
    <InfoRow :value="`${application.salary_package} LPA`" label="Package" />

    <InfoRow :value="application.job_location" label="Location" />

    <InfoRow :value="formattedAppliedDate" label="Applied On" />
  </div>
</template>

<style scoped></style>
