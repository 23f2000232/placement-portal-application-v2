<script setup>
import AppButton from '@/components/common/form/AppButton.vue'

const props = defineProps({ drive: { type: Object, required: true } })
const emit = defineEmits(['edit', 'delete', 'applications', 'submit', 'close', 'cancel'])
</script>

<template>
  <div class="card mt-4">
    <div class="card-body">
      <div class="d-flex justify-content-end gap-2">
        <AppButton v-if="props.drive.status === 'DRAFT'" :block="false" variant="primary" @click="emit('submit')"> Submit for Approval </AppButton>
        <AppButton v-if="props.drive.status === 'OPEN'" :block="false" variant="secondary" @click="emit('close')"> Close </AppButton>
        <AppButton v-if="!['CLOSED', 'CANCELLED', 'REJECTED'].includes(props.drive.status)" :block="false" variant="danger" @click="emit('cancel')"> Cancel </AppButton>
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
