<template>
  <div class="d-flex justify-content-end">
    <button class="btn btn-primary" type="button" @click="emit('view-details')">
      View Details
    </button>
  </div>
</template>

<script setup>
const emit = defineEmits(['view-details'])
</script>
