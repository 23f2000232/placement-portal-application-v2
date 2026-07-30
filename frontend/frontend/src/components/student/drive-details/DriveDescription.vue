<template>
  <div class="card mb-4">
    <div class="card-body">
      <h5 class="card-title mb-3">Description</h5>

      <p class="mb-0">
        {{ drive.description }}
      </p>
    </div>
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
