<script setup>
import { computed } from 'vue'

import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate, formatEnum } from '@/utils/formatters'

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})
const formattedJobType = computed(() => formatEnum(props.drive.job_type))

const formattedDeadline = computed(() => formatDate(props.drive.application_deadline))
</script>

<template>
  <InfoRow :value="`${props.drive.salary_package} LPA`" label="Package" />

  <InfoRow :value="formattedJobType" label="Job Type" />

  <InfoRow :value="formattedDeadline" label="Deadline" />
</template>

<style scoped></style>
