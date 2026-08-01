<script setup>
import AppButton from '@/components/common/form/AppButton.vue'
import AppInput from '@/components/common/form/AppInput.vue'
import AppTextarea from '@/components/common/form/AppTextarea.vue'
import PasswordField from '@/components/auth/PasswordField.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import { reactive, ref } from 'vue'
import authService from '@/services/auth.service.js'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  email: '',
  password: '',
  company_name: '',
  website: '',
  description: '',
  industry: '',
  contact_person: '',
  contact_email: '',
  contact_phone: '',
})
const loading = ref(false)

const error = ref('')

const success = ref('')
const submit = async () => {
  error.value = ''
  success.value = ''
  loading.value = true

  try {
    const request = {
      email: form.email,
      password: form.password,
      company_name: form.company_name,
      website: form.website,
      description: form.description,
      industry: form.industry,
      contact_person: form.contact_person,
      contact_email: form.contact_email,
      contact_phone: form.contact_phone,
    }

    await authService.registerCompany(request)

    success.value = 'Company registered successfully.'
    setTimeout(async () => {
      await router.push({
        name: 'login',
      })
    }, 2000)
    Object.assign(form, {
      email: '',
      password: '',
      company_name: '',
      website: '',
      description: '',
      industry: '',
      contact_person: '',
      contact_email: '',
      contact_phone: '',
    })
  } catch (err) {
    console.error('Company registration failed', err)

    error.value = 'Unable to register company.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form @submit.prevent="submit">
    <h2 class="text-center mb-4">Company Registration</h2>

    <ErrorAlert v-if="error" :message="error" />

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <AppInput
      id="email"
      v-model="form.email"
      label="Email"
      placeholder="Enter company email"
      required
      type="email"
    />

    <PasswordField
      id="password"
      v-model="form.password"
      label="Password"
      placeholder="Enter password"
      required
    />

    <AppInput
      id="company-name"
      v-model="form.company_name"
      label="Company Name"
      placeholder="Enter company name"
      required
    />

    <AppInput
      id="website"
      v-model="form.website"
      label="Website"
      placeholder="https://example.com"
      type="url"
    />

    <AppTextarea
      id="description"
      v-model="form.description"
      :rows="5"
      label="Company Description"
      placeholder="Describe your company"
      required
    />

    <AppInput
      id="industry"
      v-model="form.industry"
      label="Industry"
      placeholder="Information Technology"
      required
    />

    <AppInput
      id="contact-person"
      v-model="form.contact_person"
      label="Contact Person"
      placeholder="Full name"
      required
    />

    <AppInput
      id="contact-email"
      v-model="form.contact_email"
      label="Contact Email"
      placeholder="recruitment@company.com"
      required
      type="email"
    />

    <AppInput
      id="contact-phone"
      v-model="form.contact_phone"
      label="Contact Phone"
      placeholder="Enter contact number"
      required
      type="tel"
    />

    <AppButton :loading="loading" loading-text="Registering..." type="submit" variant="primary">
      Register
    </AppButton>
  </form>
</template>

<style scoped></style>
