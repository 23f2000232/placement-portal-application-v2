<template>
  <RouterLink :to="to" class="list-group-item list-group-item-action">
    {{ label }}
  </RouterLink>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    required: true,
  },

  to: {
    type: String,
    required: true,
  },
})
</script>
