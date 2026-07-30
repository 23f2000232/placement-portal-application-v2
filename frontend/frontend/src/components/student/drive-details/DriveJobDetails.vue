<script setup>
import InfoRow from '@/components/common/InfoRow.vue'
import { formatEnum, formatExperience } from '@/utils/formatters.js'

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
      <h5 class="card-title mb-3">Job Details</h5>

      <InfoRow :value="`${drive.salary_package} LPA`" label="Package" />

      <InfoRow :value="drive.job_location" label="Location" />

      <InfoRow :value="formatEnum(drive.job_type)" label="Job Type" />

      <InfoRow :value="drive.vacancies" label="Vacancies" />

      <InfoRow :value="formatExperience(drive.experience_required)" label="Experience" />
    </div>
  </div>
</template>
