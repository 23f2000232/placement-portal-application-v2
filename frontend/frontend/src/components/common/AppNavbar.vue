<template>
  <nav class="navbar navbar-expand-lg bg-dark navbar-dark px-4">
    <span class="navbar-brand"> Placement Portal </span>

    <div class="ms-auto"><button class="btn btn-outline-light btn-sm" @click="signOut">Logout</button></div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { logout } from '@/utils/auth'

const router = useRouter()
const signOut = async () => {
  logout()
  await router.push({ name: 'login' })
}
</script>
