<template>
  <div class="container-fluid p-0">
    <AppNavbar />

    <div class="row g-0">
      <aside class="col-2 border-end min-vh-100">
        <AppSidebar />
      </aside>

      <main class="col p-4">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import AppNavbar from '@/components/common/AppNavbar.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
</script>
