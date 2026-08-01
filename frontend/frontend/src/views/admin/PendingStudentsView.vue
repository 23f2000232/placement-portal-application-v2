<script setup>
import { onMounted, ref } from 'vue'
import adminService from '@/services/admin.service.js'
import EmptyState from '@/components/common/EmptyState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import StudentApprovalCard from '@/components/admin/StudentApprovalCard.vue'

const students = ref([])
const loading = ref(true)
const error = ref('')
const processingStudentId = ref(null)
const loadPendingStudents = async () => {
  error.value = ''
  loading.value = true

  try {
    students.value = await adminService.getPendingStudents()
  } catch (err) {
    console.error('Failed to load pending students', err)

    error.value = 'Failed to load pending students.'
  } finally {
    loading.value = false
  }
}

onMounted(loadPendingStudents)
const approveStudent = async (student) => {
  processingStudentId.value = student.id
  try {
    await adminService.approveStudent(student.id)

    await loadPendingStudents()
  } catch (err) {
    console.error('Failed to approve student', err)

    error.value = 'Failed to approve student.'
  } finally {
    processingStudentId.value = null
  }
}

const rejectStudent = async (student) => {
  processingStudentId.value = student.id
  try {
    await adminService.rejectStudent(student.id)

    await loadPendingStudents()
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
      <h2 class="mb-4">Pending Student Approvals</h2>

      <LoadingSpinner v-if="loading" />

      <ErrorAlert v-else-if="error" :message="error" />

      <EmptyState
        v-else-if="students.length === 0"
        message="There are no students awaiting approval."
        title="No Pending Students"
      />

      <div v-else>
        <StudentApprovalCard
          v-for="student in students"
          :key="student.id"
          :processing="processingStudentId === student.id"
          :student="student"
          @approve="approveStudent"
          @reject="rejectStudent"
        />
      </div>
    </div>
  </AppLayout>
</template>
