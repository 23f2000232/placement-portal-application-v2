<template>
  <nav class="navbar navbar-expand-lg bg-dark navbar-dark px-4">
    <span class="navbar-brand"> Placement Portal </span>

    <div class="ms-auto d-flex gap-2">
      <button v-if="canInstall" class="btn btn-outline-light btn-sm" @click="installApp">
        Install app
      </button>
      <button class="btn btn-outline-light btn-sm" @click="signOut">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout } from '@/utils/auth'

const router = useRouter()
const deferredInstallPrompt = ref(null)
const canInstall = ref(false)

const saveInstallPrompt = (event) => {
  deferredInstallPrompt.value = window.deferredPwaInstallPrompt || event?.detail
  canInstall.value = Boolean(deferredInstallPrompt.value)
}

const installApp = async () => {
  if (!deferredInstallPrompt.value) return

  deferredInstallPrompt.value.prompt()
  await deferredInstallPrompt.value.userChoice
  deferredInstallPrompt.value = null
  window.deferredPwaInstallPrompt = null
  canInstall.value = false
}

onMounted(() => {
  saveInstallPrompt()
  window.addEventListener('pwa-installable', saveInstallPrompt)
})
onBeforeUnmount(() => window.removeEventListener('pwa-installable', saveInstallPrompt))

const signOut = async () => {
  logout()
  await router.push({ name: 'login' })
}
</script>
