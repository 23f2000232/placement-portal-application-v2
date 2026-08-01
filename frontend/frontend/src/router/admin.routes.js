import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import PendingStudentsView from '@/views/admin/PendingStudentsView.vue'
import PendingCompaniesView from '@/views/admin/PendingCompaniesView.vue'

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
    component: PendingStudentsView,
    meta: {
      requiresAuth: true,
      role: 'ADMIN',
    },
  },
  {
    path: '/admin/companies',
    name: 'company-approval',
    component: PendingCompaniesView,
    meta: {
      requiresAuth: true,
      role: 'ADMIN',
    },
  },
]
