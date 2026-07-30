<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },

  message: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="text-center py-5">
    <h4 class="mb-3">
      {{ title }}
    </h4>

    <p class="text-muted">
      {{ message }}
    </p>
  </div>
</template>

<style scoped></style>
