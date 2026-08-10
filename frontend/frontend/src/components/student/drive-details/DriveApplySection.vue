<script setup>
import { computed } from 'vue'
import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate } from '@/utils/formatters.js'

const emit = defineEmits(['apply'])
const props = defineProps({
  drive: { type: Object, required: true },
  loading: { type: Boolean, default: false },
  applied: { type: Boolean, default: false },
})
const deadlinePassed = computed(() => new Date(props.drive.application_deadline) <= new Date())
</script>
<template>
  <div class="card">
    <div class="card-body">
      <InfoRow :value="formatDate(drive.application_deadline)" label="Application Deadline" />

      <div class="d-grid mt-4">
        <button
          :disabled="loading || applied || deadlinePassed"
          class="btn btn-success"
          type="button"
          @click="emit('apply')"
        >
          {{ applied ? 'Applied' : deadlinePassed ? 'Application Deadline Passed' : loading ? 'Applying...' : 'Apply Now' }}
        </button>
      </div>
    </div>
  </div>
</template>
