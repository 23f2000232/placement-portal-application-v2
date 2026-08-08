<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import driveService from '@/services/company-placement-drive.service'
import companyService from '@/services/company.service'
import { formatEnum } from '@/utils/formatters'

const drives = ref([]); const selectedDrive = ref(''); const applications = ref([]); const loading = ref(true); const error = ref(''); const updatingId = ref('')
const loadDrives = async () => { try { const result = await driveService.getCompanyPlacementDrives({ page: 1, size: 100 }); drives.value = result.items; if (drives.value.length) { selectedDrive.value = drives.value[0].id; await loadApplications() } } catch { error.value = 'Unable to load company drives.' } finally { loading.value = false } }
const loadApplications = async () => { if (!selectedDrive.value) return; loading.value = true; try { const result = await companyService.getDriveApplications(selectedDrive.value, { page: 1, size: 100 }); applications.value = result.items } catch { error.value = 'Unable to load applications.' } finally { loading.value = false } }
const update = async (application, action) => { updatingId.value = application.id; try { await companyService.updateApplicationStatus(application.id, action); await loadApplications() } catch { error.value = 'Unable to update application status.' } finally { updatingId.value = '' } }
onMounted(loadDrives)
</script>
<template><AppLayout><div class="container py-4"><h2>Drive Applications</h2><select v-model="selectedDrive" class="form-select my-4" @change="loadApplications"><option v-for="drive in drives" :key="drive.id" :value="drive.id">{{ drive.title }}</option></select>
  <LoadingSpinner v-if="loading" /><ErrorAlert v-else-if="error" :message="error" /><EmptyState v-else-if="!drives.length" title="No Drives" message="Create a placement drive to receive applications." /><EmptyState v-else-if="!applications.length" title="No Applications" message="No students have applied to this drive yet." />
  <div v-else class="table-responsive"><table class="table align-middle"><thead><tr><th>Student</th><th>Roll no.</th><th>Branch</th><th>CGPA</th><th>Status</th><th>Actions</th></tr></thead><tbody><tr v-for="application in applications" :key="application.id"><td>{{ application.student_name }}</td><td>{{ application.roll_number }}</td><td>{{ application.branch }}</td><td>{{ application.cgpa }}</td><td>{{ formatEnum(application.application_status) }}</td><td class="text-nowrap"><button class="btn btn-sm btn-outline-primary me-1" :disabled="updatingId === application.id" @click="update(application, 'under-review')">Review</button><button class="btn btn-sm btn-outline-success me-1" :disabled="updatingId === application.id" @click="update(application, 'shortlist')">Shortlist</button><button class="btn btn-sm btn-success me-1" :disabled="updatingId === application.id" @click="update(application, 'select')">Select</button><button class="btn btn-sm btn-outline-danger" :disabled="updatingId === application.id" @click="update(application, 'reject')">Reject</button></td></tr></tbody></table></div>
</div></AppLayout></template>
