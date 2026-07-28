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
  },
  {
    path: '/register/student',
    name: 'student-register',
    component: StudentRegisterView,
  },
  {
    path: '/register/company',
    name: 'company-register',
    component: CompanyRegisterView,
  },
]
