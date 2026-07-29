const ACCESS_TOKEN = 'access_token'
const REFRESH_TOKEN = 'refresh_token'
const TOKEN_TYPE = 'token_type'
const CURRENT_USER = 'current_user'

export function saveTokens(response) {
  localStorage.setItem(ACCESS_TOKEN, response.access_token)
  localStorage.setItem(REFRESH_TOKEN, response.refresh_token)
  localStorage.setItem(TOKEN_TYPE, response.token_type)
}

export function saveCurrentUser(user) {
  localStorage.setItem(CURRENT_USER, JSON.stringify(user))
}

export function getCurrentUser() {
  const user = localStorage.getItem(CURRENT_USER)

  return user ? JSON.parse(user) : null
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN)
}

export function isAuthenticated() {
  return !!getAccessToken()
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('token_type')
  localStorage.removeItem('current_user')
}

export function getDashboardRoute(role) {
  switch (role) {
    case 'STUDENT':
      return { name: 'student-dashboard' }
    case 'COMPANY':
      return { name: 'company-dashboard' }
    case 'ADMIN':
      return { name: 'admin-dashboard' }
    default:
      return { name: 'login' }
  }
}
