<template>
  <div class="row">
    <div class="col-md-4">
      <strong>Package</strong>
      <div>{{ drive.salary_package }} LPA</div>
    </div>

    <div class="col-md-4">
      <strong>Location</strong>
      <div>{{ drive.job_location }}</div>
    </div>

    <div class="col-md-4">
      <strong>Job Type</strong>
      <div>{{ formattedJobType }}</div>
    </div>
  </div>

  <hr />

  <small class="text-muted">
    Apply before:
    {{ formattedDeadline }}
  </small>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})

const formattedJobType = computed(() => props.drive.job_type.replaceAll('_', ' '))

const formattedDeadline = computed(() =>
  new Date(props.drive.application_deadline).toLocaleDateString(),
)
</script>
