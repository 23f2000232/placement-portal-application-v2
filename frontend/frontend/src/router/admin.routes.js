import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import StudentApprovalView from '@/views/admin/StudentApprovalView.vue'
import CompanyApprovalView from '@/views/admin/CompanyApprovalView.vue'

export default [
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: AdminDashboardView,
  },
  {
    path: '/admin/students',
    name: 'student-approval',
    component: StudentApprovalView,
  },
  {
    path: '/admin/companies',
    name: 'company-approval',
    component: CompanyApprovalView,
  },
]
