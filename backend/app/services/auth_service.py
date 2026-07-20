from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        student_repository: StudentRepository,
        company_repository: CompanyRepository,
    ):
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.company_repository = company_repository