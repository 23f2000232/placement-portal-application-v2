import StudentDashboardView from '@/views/student/StudentDashboardView.vue'
import StudentDrivesView from '@/views/student/StudentDrivesView.vue'
import StudentApplicationsView from '@/views/student/StudentApplicationsView.vue'
import StudentResumeView from '@/views/student/StudentResumeView.vue'
import StudentInterviewsView from '@/views/student/StudentInterviewsView.vue'

export default [
  {
    path: '/student/dashboard',
    name: 'student-dashboard',
    component: StudentDashboardView,
  },
  {
    path: '/student/drives',
    name: 'student-drives',
    component: StudentDrivesView,
  },
  {
    path: '/student/applications',
    name: 'student-applications',
    component: StudentApplicationsView,
  },
  {
    path: '/student/resume',
    name: 'student-resume',
    component: StudentResumeView,
  },
  {
    path: '/student/interviews',
    name: 'student-interviews',
    component: StudentInterviewsView,
  },
]
