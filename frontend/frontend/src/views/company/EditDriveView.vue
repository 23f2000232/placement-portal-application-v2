<script setup>
import AppLayout from '@/layouts/AppLayout.vue'
import CreateDriveForm from '@/components/company/CreateDriveForm.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template><AppLayout><div class="container py-4"><div class="row justify-content-center"><div class="col-lg-8"><CreateDriveForm :drive-id="route.params.driveId" /></div></div></div></AppLayout></template>
