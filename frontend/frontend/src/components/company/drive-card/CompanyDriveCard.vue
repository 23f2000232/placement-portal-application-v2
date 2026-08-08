<script setup>
import CompanyDriveHeader from '@/components/company/drive-card/CompanyDriveHeader.vue'
import CompanyDriveInfo from '@/components/company/drive-card/CompanyDriveInfo.vue'
import CompanyDriveActions from '@/components/company/drive-card/CompanyDriveActions.vue'

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['view', 'edit', 'delete'])
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <CompanyDriveHeader :drive="props.drive" />

      <hr />

      <CompanyDriveInfo :drive="props.drive" />

      <hr />

      <CompanyDriveActions
        @delete="emit('delete', props.drive)"
        @edit="emit('edit', props.drive)"
        @view="emit('view', props.drive)"
      />
    </div>
  </div>
</template>
