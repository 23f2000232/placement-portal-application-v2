<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <DriveHeader :drive="drive" />

      <hr />

      <DriveInfo :drive="drive" />

      <hr />

      <DriveActions @view-details="emit('view-details', drive)" />
    </div>
  </div>
</template>

<script setup>
import DriveHeader from '@/components/student/drive-card/DriveHeader.vue'
import DriveInfo from '@/components/student/drive-card/DriveInfo.vue'
import DriveActions from '@/components/student/drive-card/DriveActions.vue'

defineProps({
  drive: {
    type: Object,
    required: true,
  },
})
const emit = defineEmits(['view-details'])
</script>
