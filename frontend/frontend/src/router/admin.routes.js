import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import PendingStudentsView from '@/views/admin/PendingStudentsView.vue'
import PendingCompaniesView from '@/views/admin/PendingCompaniesView.vue'
import PendingDrivesView from '@/views/admin/PendingDrivesView.vue'
import UserManagementView from '@/views/admin/UserManagementView.vue'

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
  {
    path: '/admin/drives',
    name: 'admin-drive-approvals',
    component: PendingDrivesView,
    meta: { requiresAuth: true, role: 'ADMIN' },
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: UserManagementView,
    meta: { requiresAuth: true, role: 'ADMIN' },
  },
]
