<script setup>
const props = defineProps({
  loadingText: {
    type: String,
    default: 'Loading...',
  },

  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark'].includes(
        value,
      ),
  },

  type: {
    type: String,
    default: 'button',
  },

  loading: {
    type: Boolean,
    default: false,
  },

  disabled: {
    type: Boolean,
    default: false,
  },

  block: {
    type: Boolean,
    default: true,
  },
})
</script>

<template>
  <button
    :class="[
      'btn',
      `btn-${props.variant}`,
      {
        'w-100': props.block,
      },
    ]"
    :disabled="props.loading || props.disabled"
    :type="props.type"
  >
    <template v-if="props.loading">
      <span aria-hidden="true" class="spinner-border spinner-border-sm me-2" role="status" />

      {{ props.loadingText }}
    </template>

    <slot v-else />
  </button>
</template>

<style scoped></style>
