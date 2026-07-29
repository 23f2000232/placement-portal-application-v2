<template>
  <AuthLayout>
    <AuthCard>
      <LoginForm />
    </AuthCard>
  </AuthLayout>
</template>

<script setup>
import AuthCard from '@/components/auth/AuthCard.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import LoginForm from '@/components/auth/LoginForm.vue'
</script>
