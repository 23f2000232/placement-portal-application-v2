<script setup>
const props = defineProps({
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

  rows: {
    type: Number,
    default: 4,
  },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="mb-3">
    <label v-if="props.label" :for="props.id" class="form-label">
      {{ props.label }}
    </label>

    <textarea
      :id="props.id"
      :class="{ 'is-invalid': props.error }"
      :disabled="props.disabled"
      :placeholder="props.placeholder"
      :required="props.required"
      :rows="props.rows"
      :value="props.modelValue"
      class="form-control"
      @input="emit('update:modelValue', $event.target.value)"
    />

    <div v-if="props.error" class="invalid-feedback">
      {{ props.error }}
    </div>
  </div>
</template>

<style scoped></style>
