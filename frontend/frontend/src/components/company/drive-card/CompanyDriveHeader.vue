<script setup>

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="d-flex justify-content-between align-items-start">
    <div>
      <h5 class="card-title mb-1">
        {{ props.drive.title }}
      </h5>

      <h6 class="text-muted">
        {{ props.drive.job_location }}
      </h6>
    </div>

    <span :class="props.drive.is_remote ? 'bg-success' : 'bg-secondary'" class="badge">
      {{ props.drive.is_remote ? 'Remote' : 'On Site' }}
    </span>
  </div>
</template>

<style scoped></style>
