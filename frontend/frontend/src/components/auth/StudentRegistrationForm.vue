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
  resume_path: '',
})
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
    const request = {
      email: form.email,
      password: form.password,
      full_name: form.full_name,
      roll_number: form.roll_number,
      phone_number: form.phone_number,
      branch: form.branch,
      semester: Number(form.semester),
      cgpa: Number(form.cgpa),
      resume_path: form.resume_path,
    }

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
      resume_path: '',
    })
  } catch (err) {
    console.error('Student registration failed', err)

    error.value = 'Unable to register student.'
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
    <AppInput
      id="resume-path"
      v-model="form.resume_path"
      label="Resume Path"
      placeholder="Resume file path"
      required
    />
    <AppButton :loading="loading" loading-text="Registering..." type="submit" variant="primary">
      Register
    </AppButton>
  </form>
</template>

<style scoped></style>
