<script setup>
import AppButton from '@/components/common/form/AppButton.vue'

const emit = defineEmits(['edit', 'delete', 'applications'])
</script>

<template>
  <div class="card mt-4">
    <div class="card-body">
      <div class="d-flex justify-content-end gap-2">
        <AppButton :block="false" variant="warning" @click="emit('edit')"> Edit </AppButton>

        <AppButton :block="false" variant="danger" @click="emit('delete')"> Delete </AppButton>

        <AppButton :block="false" variant="primary" @click="emit('applications')">
          View Applications
        </AppButton>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
