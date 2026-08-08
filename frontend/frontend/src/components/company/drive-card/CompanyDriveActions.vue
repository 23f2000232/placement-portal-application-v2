<template>
  <div class="d-flex justify-content-end gap-2">
    <AppButton :block="false" variant="primary" @click="emit('view')"> View </AppButton>

    <AppButton :block="false" variant="warning" @click="emit('edit')"> Edit </AppButton>

    <AppButton :block="false" variant="danger" @click="emit('delete')"> Delete </AppButton>
  </div>
</template>

<script setup>
import AppButton from '@/components/common/form/AppButton.vue'

const emit = defineEmits(['view', 'edit', 'delete'])
</script>

<style scoped></style>
