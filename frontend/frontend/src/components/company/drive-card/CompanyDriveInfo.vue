<script setup>
import { computed } from 'vue'

import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate } from '@/utils/formatters'

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})

const formattedDeadline = computed(() => formatDate(props.drive.application_deadline))
</script>

<template>
  <InfoRow :value="`${drive.salary_package} LPA`" label="Package" />

  <InfoRow :value="drive.job_location" label="Location" />

  <InfoRow :value="drive.vacancies" label="Vacancies" />

  <InfoRow :value="formattedDeadline" label="Application Deadline" />
</template>

<style scoped></style>
