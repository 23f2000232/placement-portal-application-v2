<script setup>
import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate } from '@/utils/formatters.js'

defineProps({
  drive: {
    type: Object,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  applied: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['apply'])
</script>
<template>
  <div class="card">
    <div class="card-body">
      <InfoRow :value="formatDate(drive.application_deadline)" label="Application Deadline" />

      <div class="d-grid mt-4">
        <button
          :disabled="loading || applied"
          class="btn btn-success"
          type="button"
          @click="emit('apply')"
        >
          {{ applied ? 'Applied' : loading ? 'Applying...' : 'Apply Now' }}
        </button>
      </div>
    </div>
  </div>
</template>
