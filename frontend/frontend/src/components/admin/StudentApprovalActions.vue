<script setup>
import AppButton from '@/components/common/form/AppButton.vue'

const emit = defineEmits(['approve', 'reject'])
const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div class="d-flex justify-content-end gap-2">
    <AppButton
      :block="false"
      :loading="props.loading"
      loading-text="Approving..."
      variant="success"
      @click="emit('approve')"
    >
      Approve
    </AppButton>

    <AppButton
      :block="false"
      :loading="loading"
      loading-text="Approving..."
      variant="danger"
      @click="emit('reject')"
    >
      Reject
    </AppButton>
  </div>
</template>

<style scoped></style>
