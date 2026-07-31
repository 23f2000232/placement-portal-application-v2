<script setup>
import { computed } from 'vue'
import { formatEnum } from '@/utils/formatters'

const props = defineProps({
  application: {
    type: Object,
    required: true,
  },
})

const formattedStatus = computed(() => formatEnum(props.application.application_status))

const statusBadgeClass = computed(() => {
  switch (props.application.application_status) {
    case 'APPLIED':
      return 'bg-primary'

    case 'SHORTLISTED':
      return 'bg-success'

    case 'INTERVIEW_SCHEDULED':
      return 'bg-warning text-dark'

    case 'SELECTED':
      return 'bg-success'

    case 'REJECTED':
      return 'bg-danger'

    default:
      return 'bg-secondary'
  }
})
</script>

<template>
  <div class="d-flex justify-content-between align-items-start">
    <div>
      <h5 class="card-title mb-1">
        {{ application.job_title }}
      </h5>

      <h6 class="text-muted mb-0">
        {{ application.company_name }}
      </h6>
    </div>

    <span :class="statusBadgeClass" class="badge">
      {{ formattedStatus }}
    </span>
  </div>
</template>

<style scoped></style>
