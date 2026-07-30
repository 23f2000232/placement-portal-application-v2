<script setup>
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
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h2 class="mb-2">
            {{ drive.title }}
          </h2>

          <h5 class="text-muted">
            {{ drive.company_name }}
          </h5>
        </div>

        <span :class="drive.is_remote ? 'bg-success' : 'bg-secondary'" class="badge">
          {{ drive.is_remote ? 'Remote' : 'On Site' }}
        </span>
      </div>
    </div>
  </div>
</template>
