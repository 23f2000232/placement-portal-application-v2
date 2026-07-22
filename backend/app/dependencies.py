from app.repositories import UserRepository, StudentRepository, CompanyRepository
from app.services.auth_service import AuthService

user_repository = UserRepository()
student_repository = StudentRepository()
company_repository = CompanyRepository()

auth_service = AuthService(
    user_repository,
    student_repository,
    company_repository,
)