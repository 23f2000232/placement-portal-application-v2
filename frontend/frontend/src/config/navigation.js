export const studentNavigation = [
  {
    label: 'Dashboard',
    to: '/student/dashboard',
  },
  {
    label: 'Browse Drives',
    to: '/student/drives',
  },
  {
    label: 'Applications',
    to: '/student/applications',
  },
  {
    label: 'Resume',
    to: '/student/resume',
  },
  {
    label: 'Interviews',
    to: '/student/interviews',
  },
]
export const companyNavigation = [
  {
    label: 'Dashboard',
    to: '/company/dashboard',
  },
  {
    label: 'Placement Drives',
    to: '/company/drives',
  },
  {
    label: 'Applications',
    to: '/company/applications',
  },
  {
    label: 'Interviews',
    to: '/company/interviews',
  },
]
export const adminNavigation = [
  {
    label: 'Dashboard',
    to: '/admin/dashboard',
  },
  {
    label: 'Pending Students',
    to: '/admin/students',
  },
  {
    label: 'Pending Companies',
    to: '/admin/companies',
  },
]
export function getNavigation(role) {
  switch (role) {
    case 'STUDENT':
      return studentNavigation

    case 'COMPANY':
      return companyNavigation

    case 'ADMIN':
      return adminNavigation

    default:
      return []
  }
}
