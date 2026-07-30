<script setup>
import InfoRow from '@/components/common/InfoRow.vue'

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
      <h5 class="card-title mb-3">Eligibility</h5>

      <InfoRow :value="drive.minimum_cgpa" label="Minimum CGPA" />

      <InfoRow :value="drive.maximum_backlogs" label="Maximum Backlogs" />

      <InfoRow label="Eligible Branches">
        <span v-for="branch in drive.eligible_branches" :key="branch" class="badge bg-primary me-1">
          {{ branch }}
        </span>
      </InfoRow>
    </div>
  </div>
</template>
