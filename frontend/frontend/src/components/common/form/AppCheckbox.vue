<script setup>
defineProps({
  id: {
    type: String,
    default: '',
  },

  label: {
    type: String,
    default: '',
  },

  modelValue: {
    type: Boolean,
    default: false,
  },

  disabled: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>
<template>
  <div class="form-check mb-3">
    <input
      :id="id"
      :checked="modelValue"
      :class="{ 'is-invalid': error }"
      :disabled="disabled"
      class="form-check-input"
      type="checkbox"
      @change="emit('update:modelValue', $event.target.checked)"
    />

    <label v-if="label" :for="id" class="form-check-label">
      {{ label }}
    </label>
    <div v-if="error" class="invalid-feedback d-block">
      {{ error }}
    </div>
  </div>
</template>

<style scoped></style>
