import CompanyDashboardView from '@/views/company/CompanyDashboardView.vue'
import CompanyDrivesView from '@/views/company/CompanyDrivesView.vue'
import CompanyApplicationsView from '@/views/company/CompanyApplicationsView.vue'
import CompanyInterviewsView from '@/views/company/CompanyInterviewsView.vue'

export default [
  {
    path: '/company/dashboard',
    name: 'company-dashboard',
    component: CompanyDashboardView,
  },
  {
    path: '/company/drives',
    name: 'company-drives',
    component: CompanyDrivesView,
  },
  {
    path: '/company/applications',
    name: 'company-applications',
    component: CompanyApplicationsView,
  },
  {
    path: '/company/interviews',
    name: 'company-interviews',
    component: CompanyInterviewsView,
  },
]
