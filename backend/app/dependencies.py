from app.repositories import (
    UserRepository,
    StudentRepository,
    CompanyRepository,
    application_repository,
    placement_record_repository,
    PlacementDriveRepository,
)
from app.services.admin_service import AdminService
from app.services.auth_service import AuthService
from app.services.placement_drive_service import PlacementDriveService
from app.services.student_service import StudentService

user_repository = UserRepository()
student_repository = StudentRepository()
company_repository = CompanyRepository()
placement_drive_repository = PlacementDriveRepository()
application_repository = application_repository.ApplicationRepository()
placement_record_repository = placement_record_repository.PlacementRecordRepository()

auth_service = AuthService(user_repository, student_repository, company_repository)

admin_service = AdminService(
    student_repository=student_repository,
    company_repository=company_repository,
    user_repository=user_repository,
    placement_drive_repository=placement_drive_repository,
    application_repository=application_repository,
    placement_record_repository=placement_record_repository,
)

placement_drive_service = PlacementDriveService(
    placement_drive_repository=placement_drive_repository,
    company_repository=company_repository,
)

student_service = StudentService(
    student_repository,
    placement_drive_repository,
    company_repository,
    application_repository,
)