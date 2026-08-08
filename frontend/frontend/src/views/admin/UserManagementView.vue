<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import adminService from '@/services/admin.service'
import { formatEnum } from '@/utils/formatters'

const users = ref([]); const search = ref(''); const loading = ref(true); const error = ref(''); const processingId = ref('')
const load = async () => { loading.value = true; error.value = ''; try { const response = await adminService.getUsers({ page: 1, size: 100, search: search.value || undefined }); users.value = response.items } catch { error.value = 'Unable to load users.' } finally { loading.value = false } }
const setStatus = async (user, status) => { processingId.value = user.id; try { await adminService.setUserAccountStatus(user.id, status); await load() } catch { error.value = 'Unable to update account status.' } finally { processingId.value = '' } }
onMounted(load)
</script>

<template><AppLayout><div class="container py-4"><h2>User Management</h2><form class="input-group my-4" @submit.prevent="load"><input v-model.trim="search" class="form-control" placeholder="Search by email"><button class="btn btn-primary">Search</button></form>
  <LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!users.length" title="No Users" message="No users match this search." />
  <div v-else class="table-responsive"><table class="table align-middle"><thead><tr><th>Email</th><th>Role</th><th>Status</th><th>Action</th></tr></thead><tbody><tr v-for="user in users" :key="user.id"><td>{{ user.email }}</td><td>{{ formatEnum(user.role) }}</td><td>{{ formatEnum(user.account_status) }}</td><td><select class="form-select form-select-sm" :disabled="processingId === user.id" :value="user.account_status" @change="setStatus(user, $event.target.value)"><option value="ACTIVE">Active</option><option value="SUSPENDED">Suspended</option><option value="BLACKLISTED">Blacklisted</option></select></td></tr></tbody></table></div>
</div></AppLayout></template>
