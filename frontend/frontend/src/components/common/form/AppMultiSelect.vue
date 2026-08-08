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

  options: {
    type: Array,
    default: () => [],
  },

  modelValue: {
    type: Array,
    default: () => [],
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

const toggleOption = (value) => {
  const updated = [...props.modelValue]

  const index = updated.indexOf(value)

  if (index === -1) {
    updated.push(value)
  } else {
    updated.splice(index, 1)
  }

  emit('update:modelValue', updated)
}
</script>

<template>
  <div class="mb-3">
    <label v-if="label" class="form-label">
      {{ label }}
    </label>

    <div class="border rounded p-3">
      <div v-for="option in props.options" :key="option.value" class="form-check">
        <input
          :id="`${id}-${option.value}`"
          :checked="props.modelValue.includes(option.value)"
          :disabled="disabled"
          class="form-check-input"
          type="checkbox"
          @change="toggleOption(option.value)"
        />

        <label :for="`${id}-${option.value}`" class="form-check-label">
          {{ option.label }}
        </label>
      </div>
    </div>

    <div v-if="error" class="invalid-feedback d-block">
      {{ error }}
    </div>
  </div>
</template>

<style scoped></style>
