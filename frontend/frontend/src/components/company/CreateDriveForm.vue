<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import AppButton from '@/components/common/form/AppButton.vue'
import AppCheckbox from '@/components/common/form/AppCheckbox.vue'
import AppDateTimeInput from '@/components/common/form/AppDateTimeInput.vue'
import AppInput from '@/components/common/form/AppInput.vue'
import AppMultiSelect from '@/components/common/form/AppMultiSelect.vue'
import AppSelect from '@/components/common/form/AppSelect.vue'
import AppTextarea from '@/components/common/form/AppTextarea.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'

import branches from '@/constants/branches'
import CompanyPlacementDriveService from '@/services/company-placement-drive.service.js'

const router = useRouter()
const props = defineProps({ driveId: { type: String, default: '' } })
const isEdit = () => Boolean(props.driveId)

const form = reactive({
  title: '',
  description: '',
  job_location: '',
  is_remote: false,
  salary_package: '',
  minimum_cgpa: '',
  eligible_branches: [],
  maximum_backlogs: 0,
  experience_required: 0,
  vacancies: '',
  application_deadline: '',
  interview_date: '',
  job_type: '',
  interview_mode: '',
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const jobTypes = [
  { label: 'Full Time', value: 'FULL_TIME' },
  { label: 'Intern', value: 'INTERN' },
  { label: 'Internship with PPO', value: 'INTERNSHIP_WITH_PPO' },
]

const interviewModes = [
  { label: 'Online', value: 'ONLINE' },
  { label: 'Offline', value: 'OFFLINE' },
]

const submit = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const request = Object.fromEntries(
      Object.entries(form).filter(([, value]) => {
        if (value === '') return false
        return value !== null
      }),
    )

    if (isEdit()) await CompanyPlacementDriveService.updatePlacementDrive(props.driveId, request)
    else await CompanyPlacementDriveService.createPlacementDrive(request)

    success.value = `Placement drive ${isEdit() ? 'updated' : 'created'} successfully.`

    setTimeout(async () => {
      await router.push({
        name: 'company-drives',
      })
    }, 1500)
  } catch (err) {
    console.error(err)

    error.value = 'Failed to create placement drive.'
  } finally {
    loading.value = false
  }
}
onMounted(async () => {
  if (!isEdit()) return
  loading.value = true
  try {
    const drive = await CompanyPlacementDriveService.getCompanyPlacementDrive(props.driveId)
    Object.assign(form, {
      ...drive,
      application_deadline: drive.application_deadline?.slice(0, 16) || '',
      interview_date: drive.interview_date?.slice(0, 16) || '',
    })
  } catch (err) { error.value = err.response?.data?.message || 'Failed to load placement drive.' } finally { loading.value = false }
})
</script>

<template>
  <form @submit.prevent="submit">
    <h2 class="text-center mb-4">{{ isEdit() ? 'Edit Placement Drive' : 'Create Placement Drive' }}</h2>

    <ErrorAlert v-if="error" :message="error" />

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <!-- Basic Information -->

    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title mb-3">Basic Information</h5>

        <AppInput
          id="title"
          v-model="form.title"
          label="Job Title"
          placeholder="Software Engineer"
          required
        />

        <AppTextarea
          id="description"
          v-model="form.description"
          :rows="6"
          label="Description"
          placeholder="Describe the role..."
          required
        />

        <AppInput
          id="location"
          v-model="form.job_location"
          label="Job Location"
          placeholder="Pune"
          required
        />

        <AppCheckbox id="remote" v-model="form.is_remote" label="Remote Position" />
      </div>
    </div>

    <!-- Job Details -->

    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title mb-3">Job Details</h5>

        <AppInput
          id="package"
          v-model="form.salary_package"
          label="Salary Package (LPA)"
          required
          step="0.01"
          type="number"
        />

        <AppSelect
          id="job-type"
          v-model="form.job_type"
          :options="jobTypes"
          label="Job Type"
          required
        />

        <AppInput
          id="vacancies"
          v-model="form.vacancies"
          label="Vacancies"
          required
          type="number"
        />

        <AppInput
          id="experience"
          v-model="form.experience_required"
          label="Experience Required (Years)"
          required
          type="number"
        />
      </div>
    </div>

    <!-- Eligibility -->

    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title mb-3">Eligibility</h5>

        <AppInput
          id="cgpa"
          v-model="form.minimum_cgpa"
          label="Minimum CGPA"
          required
          step="0.01"
          type="number"
        />

        <AppInput
          id="backlogs"
          v-model="form.maximum_backlogs"
          label="Maximum Backlogs"
          required
          type="number"
        />

        <AppMultiSelect
          id="branches"
          v-model="form.eligible_branches"
          :options="branches"
          label="Eligible Branches"
          required
        />
      </div>
    </div>

    <!-- Hiring Process -->

    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title mb-3">Hiring Process</h5>

        <AppDateTimeInput
          id="deadline"
          v-model="form.application_deadline"
          label="Application Deadline"
          required
        />

        <AppDateTimeInput
          id="interview-date"
          v-model="form.interview_date"
          label="Interview Date"
        />

        <AppSelect
          id="interview-mode"
          v-model="form.interview_mode"
          :options="interviewModes"
          label="Interview Mode"
          required
        />
      </div>
    </div>

    <AppButton :loading="loading" :loading-text="isEdit() ? 'Saving Drive...' : 'Creating Drive...'" type="submit" variant="primary">
      {{ isEdit() ? 'Save Changes' : 'Create Placement Drive' }}
    </AppButton>
  </form>
</template>

<style scoped></style>
