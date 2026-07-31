<script setup>
import InfoRow from '@/components/common/InfoRow.vue'
import { formatDate, formatEnum } from '@/utils/formatters.js'

defineProps({
  drive: {
    type: Object,
    required: true,
  },
})
</script>
<template>
  <div class="card mb-4">
    <div class="card-body">
      <h5 class="card-title mb-3">Hiring Process</h5>

      <InfoRow :value="formatEnum(drive.interview_mode)" label="Interview Mode" />

      <InfoRow :value="formatDate(drive.interview_date, 'Not Scheduled')" label="Interview Date" />
    </div>
  </div>
</template>
