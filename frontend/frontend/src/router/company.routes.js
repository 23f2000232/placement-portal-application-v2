import CompanyDashboardView from '@/views/company/CompanyDashboardView.vue'
import CompanyPlacementDrivesView from '@/views/company/CompanyPlacementDrivesView.vue'
import CompanyApplicationsView from '@/views/company/CompanyApplicationsView.vue'
import CompanyInterviewsView from '@/views/company/CompanyInterviewsView.vue'
import CompanyDriveDetailsView from '@/views/company/CompanyDriveDetailsView.vue'
import CreateDriveView from '@/views/company/CreateDriveView.vue'
import EditDriveView from '@/views/company/EditDriveView.vue'

export default [
  {
    path: '/company/drives/:driveId/edit',
    name: 'company-drive-edit',
    component: EditDriveView,
    meta: { requiresAuth: true, role: 'COMPANY' },
  },
  {
    path: '/company/dashboard',
    name: 'company-dashboard',
    component: CompanyDashboardView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
  {
    path: '/company/drives',
    name: 'company-drives',
    component: CompanyPlacementDrivesView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
  {
    path: '/company/drives/:driveId',
    name: 'company-drive-details',
    component: CompanyDriveDetailsView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
  {
    path: '/company/drives/new',
    name: 'create-company-drive',
    component: CreateDriveView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
  {
    path: '/company/applications',
    name: 'company-applications',
    component: CompanyApplicationsView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
  {
    path: '/company/interviews',
    name: 'company-interviews',
    component: CompanyInterviewsView,
    meta: {
      requiresAuth: true,
      role: 'COMPANY',
    },
  },
]
