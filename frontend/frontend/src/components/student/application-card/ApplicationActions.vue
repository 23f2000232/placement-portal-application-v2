<script setup>
const emit = defineEmits(['view-details'])
</script>
<template>
  <div class="d-flex justify-content-end">
    <button class="btn btn-primary" type="button" @click="emit('view-details')">View Drive</button>
  </div>
</template>

<style scoped></style>
