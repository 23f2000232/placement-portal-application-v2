<script setup>
import { computed } from 'vue'
import { formatEnum } from '@/utils/formatters.js'
import InfoRow from '@/components/common/InfoRow.vue'
import CompanyApprovalActions from '@/components/admin/CompanyApprovalActions.vue'

const props = defineProps({
  company: {
    type: Object,
    required: true,
  },

  processing: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['approve', 'reject'])

const formattedStatus = computed(() => formatEnum(props.company.approval_status))
</script>

<template>
  <div class="card shadow-sm mb-3">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <div>
          <h5 class="card-title mb-1">
            {{ props.company.company_name }}
          </h5>

          <small class="text-muted">
            {{ props.company.email }}
          </small>
        </div>

        <span class="badge bg-warning text-dark">
          {{ formattedStatus }}
        </span>
      </div>

      <InfoRow :value="props.company.industry" label="Industry" />

      <InfoRow :value="props.company.website" label="Website" />

      <hr />

      <CompanyApprovalActions
        :loading="props.processing"
        @approve="emit('approve', props.company)"
        @reject="emit('reject', props.company)"
      />
    </div>
  </div>
</template>

<style scoped></style>
