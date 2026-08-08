<script setup>
import { onMounted, ref } from 'vue'
import adminService from '@/services/admin.service.js'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'

const students = ref([])
const loading = ref(true)
const success = ref('')
const error = ref('')
const processingStudentId = ref(null)
const filters = ref({ search: '', branch: '', semester: '', approval_status: '' })
const loadPendingStudents = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await adminService.getStudents({ page: 1, size: 100, ...filters.value })
    students.value = response.items
  } catch (err) {
    console.error('Failed to load pending students', err)

    error.value = 'Failed to load pending students.'
  } finally {
    loading.value = false
  }
}

const setAccountStatus = async (student, accountStatus) => {
  processingStudentId.value = student.id
  error.value = ''
  try {
    await adminService.setUserAccountStatus(student.user_id, accountStatus)
    await loadPendingStudents()
    success.value = 'Student account updated successfully.'
  } catch { error.value = 'Failed to update the student account.' } finally { processingStudentId.value = null }
}

onMounted(loadPendingStudents)
const approveStudent = async (student) => {
  processingStudentId.value = student.id
  error.value = ''
  success.value = ''
  try {
    await adminService.approveStudent(student.id)

    await loadPendingStudents()
    success.value = 'Student approved successfully.'
  } catch (err) {
    console.error('Failed to approve student', err)

    error.value = 'Failed to approve student.'
  } finally {
    processingStudentId.value = null
  }
}

const rejectStudent = async (student) => {
  processingStudentId.value = student.id
  error.value = ''
  success.value = ''
  try {
    await adminService.rejectStudent(student.id)

    await loadPendingStudents()
    success.value = 'Student rejected successfully.'
  } catch (err) {
    console.error('Failed to reject student', err)

    error.value = 'Failed to reject student.'
  } finally {
    processingStudentId.value = null
  }
}
</script>
<template>
  <AppLayout>
    <div class="container py-4">
      <h2 class="mb-4">Student Management</h2>
      <form class="row g-2 mb-4" @submit.prevent="loadPendingStudents">
        <div class="col-md-4"><input v-model.trim="filters.search" class="form-control" placeholder="Search name, roll number, or phone" /></div>
        <div class="col-md-3"><input v-model.trim="filters.branch" class="form-control" placeholder="Filter by branch" /></div>
        <div class="col-md-2"><input v-model.number="filters.semester" min="1" type="number" class="form-control" placeholder="Semester" /></div>
        <div class="col-md-2"><select v-model="filters.approval_status" class="form-select"><option value="">All approval states</option><option value="PENDING">Pending</option><option value="APPROVED">Approved</option><option value="REJECTED">Rejected</option></select></div>
        <div class="col-md-1"><button class="btn btn-primary w-100">Search</button></div>
      </form>
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>
      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <EmptyState
        v-else-if="students.length === 0"
        message="No students match the selected filters."
        title="No Students"
      />

      <div v-else class="table-responsive"><table class="table align-middle"><thead><tr><th>Student</th><th>Academic details</th><th>Approval</th><th>Account</th><th>Actions</th></tr></thead><tbody><tr v-for="student in students" :key="student.id"><td><div>{{ student.full_name }}</div><small class="text-muted">{{ student.email }} · {{ student.roll_number }}</small></td><td>{{ student.branch }} · Sem {{ student.semester }}<br><small>CGPA {{ student.cgpa }}</small></td><td>{{ student.approval_status }}</td><td><select class="form-select form-select-sm" :disabled="processingStudentId === student.id" :value="student.account_status" @change="setAccountStatus(student, $event.target.value)"><option value="ACTIVE">Active</option><option value="SUSPENDED">Deactivated</option><option value="BLACKLISTED">Blacklisted</option></select></td><td><template v-if="student.approval_status === 'PENDING'"><button class="btn btn-sm btn-success me-2" :disabled="processingStudentId === student.id" @click="approveStudent(student)">Approve</button><button class="btn btn-sm btn-outline-danger" :disabled="processingStudentId === student.id" @click="rejectStudent(student)">Reject</button></template></td></tr></tbody></table></div>
    </div>
  </AppLayout>
</template>
