<template>
  <AuthLayout>
    <AuthCard>
      <LoginForm />
      <div class="d-flex justify-content-between">
        <div class="text-center mt-3">
          <RouterLink :to="{ name: 'student-register' }"> Student Registration </RouterLink>
        </div>
        <div class="text-center mt-3">
          <RouterLink :to="{ name: 'company-register' }"> Company Registration </RouterLink>
        </div>
      </div>
    </AuthCard>
  </AuthLayout>
</template>

<script setup>
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'
</script>
