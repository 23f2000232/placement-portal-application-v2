<script setup>
import AppButton from '@/components/common/form/AppButton.vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['approve', 'reject'])
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
      :loading="props.loading"
      loading-text="Rejecting..."
      variant="danger"
      @click="emit('reject')"
    >
      Reject
    </AppButton>
  </div>
</template>
