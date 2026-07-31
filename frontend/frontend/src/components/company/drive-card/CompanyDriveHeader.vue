<script setup>
import { computed } from 'vue'
import { formatDate, formatEnum } from '@/utils/formatters'

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})

const formattedCreatedAt = computed(() => formatDate(props.drive.created_at))

const formattedStatus = computed(() => formatEnum(props.drive.status))

const statusBadgeClass = computed(() => {
  switch (props.drive.status) {
    case 'DRAFT':
      return 'bg-secondary'

    case 'OPEN':
      return 'bg-success'

    case 'CLOSED':
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
        {{ drive.title }}
      </h5>

      <small class="text-muted"> Created {{ formattedCreatedAt }} </small>
    </div>

    <span :class="statusBadgeClass" class="badge">
      {{ formattedStatus }}
    </span>
  </div>
</template>

<style scoped></style>
