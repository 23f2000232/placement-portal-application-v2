<template>
  <div class="d-flex justify-content-end gap-2">
    <button class="btn btn-outline-primary" type="button" @click="emit('view')">View</button>

    <button class="btn btn-primary" type="button" @click="emit('edit')">Edit</button>
  </div>
</template>

<script setup>
const emit = defineEmits(['view', 'edit'])
</script>

<style scoped></style>
