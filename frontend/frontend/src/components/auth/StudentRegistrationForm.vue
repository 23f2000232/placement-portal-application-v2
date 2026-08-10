<script setup>
import { reactive, ref } from 'vue'
import AppButton from '@/components/common/form/AppButton.vue'
import AppInput from '@/components/common/form/AppInput.vue'
import AppSelect from '@/components/common/form/AppSelect.vue'
import PasswordField from '@/components/auth/PasswordField.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import authService from '@/services/auth.service.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({
  email: '',
  password: '',
  full_name: '',
  roll_number: '',
  phone_number: '',
  branch: '',
  semester: '',
  cgpa: '',
})
const resumeFile = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref('')
const branches = [
  {
    label: 'Computer Science',
    value: 'CS',
  },
  {
    label: 'Information Technology',
    value: 'IT',
  },
  {
    label: 'Electronics',
    value: 'EXTC',
  },
  {
    label: 'Mechanical',
    value: 'MECH',
  },
  {
    label: 'Civil',
    value: 'CIVIL',
  },
]
const semesters = Array.from({ length: 8 }, (_, index) => ({
  label: `${index + 1}`,
  value: index + 1,
}))
const submit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    if (!resumeFile.value) {
      error.value = 'Please select a PDF resume.'
      return
    }
    if (resumeFile.value.type && resumeFile.value.type !== 'application/pdf') {
      error.value = 'Only PDF files are allowed.'
      return
    }
    const request = new FormData()
    request.append('email', form.email)
    request.append('password', form.password)
    request.append('full_name', form.full_name)
    request.append('roll_number', form.roll_number)
    request.append('phone_number', form.phone_number)
    request.append('branch', form.branch)
    request.append('semester', String(Number(form.semester)))
    request.append('cgpa', String(Number(form.cgpa)))
    request.append('resume', resumeFile.value)

    await authService.registerStudent(request)

    success.value = 'Registration successful.'
    setTimeout(async () => {
      await router.push({
        name: 'login',
      })
    }, 2000)
    Object.assign(form, {
      email: '',
      password: '',
      full_name: '',
      roll_number: '',
      phone_number: '',
      branch: '',
      semester: '',
      cgpa: '',
    })
    resumeFile.value = null
  } catch (err) {
    console.error('Student registration failed', err)

    error.value = err.response?.data?.message || 'Unable to register student.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="submit">
    <h2 class="text-center mb-4">Student Registration</h2>
    <ErrorAlert v-if="error" :message="error" />

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>
    <AppInput
      id="email"
      v-model="form.email"
      label="Email"
      placeholder="Enter your email"
      required
      type="email"
    />
    <PasswordField
      id="password"
      v-model="form.password"
      label="Password"
      placeholder="Enter your password"
      required
    />
    <AppInput
      id="full-name"
      v-model="form.full_name"
      label="Full Name"
      placeholder="Enter your full name"
      required
    />
    <AppInput
      id="roll-number"
      v-model="form.roll_number"
      label="Roll Number"
      placeholder="Enter your roll number"
      required
    />
    <AppInput
      id="phone-number"
      v-model="form.phone_number"
      label="Phone Number"
      placeholder="Enter your phone number"
      required
      type="tel"
    />
    <AppSelect id="branch" v-model="form.branch" :options="branches" label="Branch" required />
    <AppSelect
      id="semester"
      v-model="form.semester"
      :options="semesters"
      label="Semester"
      required
    />
    <AppInput
      id="cgpa"
      v-model="form.cgpa"
      label="CGPA"
      max="10"
      min="0"
      placeholder="Enter your CGPA"
      required
      step="0.01"
      type="number"
    />
    <div class="mb-3">
      <label for="resume" class="form-label">Resume (PDF)</label>
      <input id="resume" accept="application/pdf,.pdf" class="form-control" required type="file" @change="resumeFile = $event.target.files?.[0] || null" />
      <div class="form-text">Upload your resume as a PDF file.</div>
    </div>
    <AppButton :loading="loading" loading-text="Registering..." type="submit" variant="primary">
      Register
    </AppButton>
  </form>
</template>

<style scoped></style>
