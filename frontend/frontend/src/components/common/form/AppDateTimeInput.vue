<script setup>
import AppInput from '@/components/common/form/AppInput.vue'

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
    type: String,
    default: '',
  },

  placeholder: {
    type: String,
    default: '',
  },

  required: {
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
  <AppInput
    :id="id"
    :disabled="disabled"
    :error="error"
    :label="label"
    :model-value="modelValue"
    :placeholder="placeholder"
    :required="required"
    type="datetime-local"
    @update:model-value="emit('update:modelValue', $event)"
  />
</template>

<style scoped></style>
