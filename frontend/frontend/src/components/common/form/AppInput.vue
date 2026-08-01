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
    type: [String, Number],
    default: '',
  },

  type: {
    type: String,
    default: 'text',
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
  min: {
    type: [String, Number],
    default: undefined,
  },

  max: {
    type: [String, Number],
    default: undefined,
  },

  step: {
    type: [String, Number],
    default: undefined,
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="mb-3">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
    </label>

    <input
      :id="id"
      :class="{ 'is-invalid': error }"
      :disabled="disabled"
      :max="max"
      :min="min"
      :placeholder="placeholder"
      :required="required"
      :step="step"
      :type="type"
      :value="modelValue"
      class="form-control"
      @input="emit('update:modelValue', $event.target.value)"
    />

    <div v-if="error" class="invalid-feedback">
      {{ error }}
    </div>
  </div>
</template>

<style scoped></style>
