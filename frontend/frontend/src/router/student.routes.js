import StudentDashboardView from '@/views/student/StudentDashboardView.vue'
import StudentDrivesView from '@/views/student/StudentDrivesView.vue'
import StudentApplicationsView from '@/views/student/StudentApplicationsView.vue'
import StudentResumeView from '@/views/student/StudentResumeView.vue'
import StudentInterviewsView from '@/views/student/StudentInterviewsView.vue'
import StudentDriveDetailsView from '@/views/student/StudentDriveDetailsView.vue'
import StudentApplicationDetailsView from '@/views/student/StudentApplicationDetailsView.vue'

export default [
  {
    path: '/student/dashboard',
    name: 'student-dashboard',
    component: StudentDashboardView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/drives',
    name: 'student-drives',
    component: StudentDrivesView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/applications',
    name: 'student-applications',
    component: StudentApplicationsView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/applications/:applicationId',
    name: 'student-application-details',
    component: StudentApplicationDetailsView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/resume',
    name: 'student-resume',
    component: StudentResumeView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/interviews',
    name: 'student-interviews',
    component: StudentInterviewsView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
  {
    path: '/student/drives/:driveId',
    name: 'student-drive-details',
    component: StudentDriveDetailsView,
    meta: {
      requiresAuth: true,
      role: 'STUDENT',
    },
  },
]
