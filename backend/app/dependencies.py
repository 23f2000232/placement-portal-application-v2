from app.repositories import (
    UserRepository,
    StudentRepository,
    CompanyRepository,
    application_repository,
    placement_record_repository,
    PlacementDriveRepository,
    InterviewRepository,
)
from app.services import interview_service
from app.services.admin_service import AdminService
from app.services.auth_service import AuthService
from app.services.company_service import CompanyService
from app.services.placement_drive_service import PlacementDriveService
from app.services.storage.local_storage_service import LocalStorageService
from app.services.student_service import StudentService

user_repository = UserRepository()
student_repository = StudentRepository()
company_repository = CompanyRepository()
placement_drive_repository = PlacementDriveRepository()
application_repository = application_repository.ApplicationRepository()
placement_record_repository = placement_record_repository.PlacementRecordRepository()
storage_service = LocalStorageService()
interview_repository = InterviewRepository()

auth_service = AuthService(user_repository, student_repository, company_repository, storage_service)

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
    storage_service,
)

company_service = CompanyService(
    company_repository, placement_drive_repository, application_repository, interview_repository
)

interview_service = interview_service.InterviewService(
    interview_repository,
    application_repository,
    placement_drive_repository,
    student_repository,
    company_repository,
)
