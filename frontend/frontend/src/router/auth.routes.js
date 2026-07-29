import LoginView from '@/views/auth/LoginView.vue'
import StudentRegisterView from '@/views/auth/StudentRegisterView.vue'
import CompanyRegisterView from '@/views/auth/CompanyRegisterView.vue'

export default [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guest: true,
    },
  },
  {
    path: '/register/student',
    name: 'student-register',
    component: StudentRegisterView,
    meta: {
      guest: true,
    },
  },
  {
    path: '/register/company',
    name: 'company-register',
    component: CompanyRegisterView,
    meta: {
      guest: true,
    },
  },
]
