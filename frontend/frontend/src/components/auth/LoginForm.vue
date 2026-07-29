<script setup>
import { ref } from 'vue'

import authService from '@/services/auth.service'
import { saveCurrentUser, saveTokens } from '@/utils/auth.js'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')

const loading = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''
  loading.value = true

  try {
    const loginRequest = {
      email: email.value,
      password: password.value,
    }

    const response = await authService.login(loginRequest)
    saveTokens(response)
    const currentUser = await authService.getCurrentUser()
    saveCurrentUser(currentUser)

    switch (currentUser.role) {
      case 'STUDENT':
        await router.push('/student/dashboard')
        break

      case 'COMPANY':
        await router.push('/company/dashboard')
        break

      case 'ADMIN':
        await router.push('/admin/dashboard')
        break

      default:
        error.value = 'Unknown user role.'
    }

    console.log(currentUser)
  } catch (err) {
    error.value = 'Invalid email or password.'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
<template>
  <form @submit.prevent="submit">
    <h2 class="text-center mb-4">Placement Portal</h2>

    <div class="mb-3">
      <label class="form-label" for="email"> Email </label>

      <input id="email" v-model="email" class="form-control" type="email" />
    </div>

    <div class="mb-4">
      <label class="form-label" for="password"> Password </label>

      <input id="password" v-model="password" class="form-control" type="password" />
    </div>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <button :disabled="loading" class="btn btn-primary w-100" type="submit">
      {{ loading ? 'Logging in...' : 'Login' }}
    </button>
  </form>
</template>
