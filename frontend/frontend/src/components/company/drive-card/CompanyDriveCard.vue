<script setup>
import CompanyDriveHeader from '@/components/company/drive-card/CompanyDriveHeader.vue'
import CompanyDriveInfo from '@/components/company/drive-card/CompanyDriveInfo.vue'
import CompanyDriveActions from '@/components/company/drive-card/CompanyDriveActions.vue'

defineProps({
  drive: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['view', 'edit'])
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <CompanyDriveHeader :drive="drive" />

      <hr />

      <CompanyDriveInfo :drive="drive" />

      <hr />

      <CompanyDriveActions @edit="emit('edit', drive)" @view="emit('view', drive)" />
    </div>
  </div>
</template>

<style scoped></style>
