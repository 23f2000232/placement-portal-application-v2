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
    type: [String, Number],
    default: '',
  },

  options: {
    type: Array,
    default: () => [],
  },

  placeholder: {
    type: String,
    default: 'Select an option',
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
  <div class="mb-3">
    <label v-if="props.label" :for="props.id" class="form-label">
      {{ props.label }}
    </label>

    <select
      :id="props.id"
      :class="{ 'is-invalid': props.error }"
      :disabled="props.disabled"
      :required="props.required"
      :value="props.modelValue"
      class="form-select"
      @change="emit('update:modelValue', $event.target.value)"
    >
      <option disabled value="">
        {{ props.placeholder }}
      </option>

      <option v-for="option in props.options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>

    <div v-if="props.error" class="invalid-feedback">
      {{ props.error }}
    </div>
  </div>
</template>

<style scoped></style>
