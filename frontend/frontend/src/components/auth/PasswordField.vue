<script setup>
import { computed, ref } from 'vue'
import AppInput from '@/components/common/form/AppInput.vue'

const visible = ref(false)
const inputType = computed(() => (visible.value ? 'text' : 'password'))
const emit = defineEmits(['update:modelValue'])
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
</script>

<template>
  <AppInput
    :id="props.id"
    :disabled="props.disabled"
    :error="props.error"
    :label="props.label"
    :model-value="props.modelValue"
    :placeholder="props.placeholder"
    :required="props.required"
    :type="inputType"
    @update:model-value="emit('update:modelValue', $event)"
  />
  <div class="text-end mt-1">
    <button
      :aria-label="visible ? 'Hide password' : 'Show password'"
      class="btn btn-link btn-sm p-0"
      type="button"
      @click="visible = !visible"
    >
      {{ visible ? 'Hide Password' : 'Show Password' }}
    </button>
  </div>
</template>

<style scoped></style>
