<template>
  <AuthLayout>
    <AuthCard>
      <LoginForm />
      <div class="text-center mt-3">
        <RouterLink :to="{ name: 'student-register' }"> Register as Student </RouterLink>
      </div>
    </AuthCard>
  </AuthLayout>
</template>

<script setup>
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'
</script>
