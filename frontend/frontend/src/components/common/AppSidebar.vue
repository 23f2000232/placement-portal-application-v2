<template>
  <div class="list-group list-group-flush">
    <SidebarItem v-for="item in navigation" :key="item.to" :label="item.label" :to="item.to" />
  </div>
</template>

<script setup>
import SidebarItem from './SidebarItem.vue'
import { getCurrentUser } from '@/utils/auth.js'
import { getNavigation } from '@/config/navigation.js'

const currentUser = getCurrentUser()
const navigation = getNavigation(currentUser.role)
</script>
