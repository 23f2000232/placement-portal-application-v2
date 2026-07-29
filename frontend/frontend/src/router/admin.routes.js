import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import StudentApprovalView from '@/views/admin/StudentApprovalView.vue'
import CompanyApprovalView from '@/views/admin/CompanyApprovalView.vue'

export default [
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboardView,
    meta: {
      requiresAuth: true,
      role: 'ADMIN',
    },
  },
  {
    path: '/admin/students',
    name: 'student-approval',
    component: StudentApprovalView,
    meta: {
      requiresAuth: true,
      role: 'ADMIN',
    },
  },
  {
    path: '/admin/companies',
    name: 'company-approval',
    component: CompanyApprovalView,
    meta: {
      requiresAuth: true,
      role: 'ADMIN',
    },
  },
]
