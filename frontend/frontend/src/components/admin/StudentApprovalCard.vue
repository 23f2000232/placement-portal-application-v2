<script setup>
import InfoRow from '@/components/common/InfoRow.vue'
import { computed } from 'vue'
import { formatEnum } from '@/utils/formatters.js'
import StudentApprovalActions from '@/components/admin/StudentApprovalActions.vue'

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
  processing: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['approve', 'reject'])

const formattedStatus = computed(() => formatEnum(props.student.approval_status))
const formattedCgpa = computed(() => Number(props.student.cgpa).toFixed(2))
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <div>
          <h5 class="card-title mb-1">
            {{ props.student.full_name }}
          </h5>

          <small class="text-muted">
            {{ props.student.email }}
          </small>
        </div>

        <span class="badge bg-warning text-dark">
          {{ formattedStatus }}
        </span>
      </div>

      <InfoRow :value="props.student.roll_number" label="Roll Number" />

      <InfoRow :value="props.student.branch" label="Branch" />

      <InfoRow :value="props.student.semester" label="Semester" />

      <InfoRow :value="formattedCgpa" label="CGPA" />

      <hr />

      <StudentApprovalActions
        :loading="props.processing"
        @approve="emit('approve', props.student)"
        @reject="emit('reject', props.student)"
      />
    </div>
  </div>
</template>

<style scoped></style>
