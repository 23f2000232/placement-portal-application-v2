<template>
  <div class="d-flex justify-content-between align-items-start">
    <div>
      <h5 class="card-title mb-1">
        {{ drive.title }}
      </h5>

      <h6 class="text-muted">
        {{ drive.company_name }}
      </h6>
    </div>

    <span :class="drive.is_remote ? 'bg-success' : 'bg-secondary'" class="badge">
      {{ drive.is_remote ? 'Remote' : 'On Site' }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  drive: {
    type: Object,
    required: true,
  },
})
</script>
