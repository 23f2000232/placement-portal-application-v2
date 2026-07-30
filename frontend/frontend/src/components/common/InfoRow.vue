<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },

  value: {
    type: [String, Number],
    required: false,
    default: '',
  },
})
</script>
<template>
  <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
    <span class="fw-semibold">
      {{ label }}
    </span>

    <div>
      <slot>
        <span class="text-muted">
          {{ value }}
        </span>
      </slot>
    </div>
  </div>
</template>
