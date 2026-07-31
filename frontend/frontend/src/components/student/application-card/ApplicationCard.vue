<script setup>
import ApplicationHeader from '@/components/student/application-card/ApplicationHeader.vue'
import ApplicationInfo from '@/components/student/application-card/ApplicationInfo.vue'

defineProps({
  application: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['view-details'])
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-header bg-white">
      <ApplicationHeader :application="application" />
    </div>

    <div class="card-body">
      <ApplicationInfo :application="application" />
    </div>

    <!--    <div class="card-footer bg-white">-->
    <!--      <ApplicationActions @view-details="emit('view-details', application)" />-->
    <!--    </div>-->
  </div>
</template>

<style scoped></style>
