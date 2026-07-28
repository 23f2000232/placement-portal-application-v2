from abc import ABC, abstractmethod


class StorageService(ABC):

    @abstractmethod
    def upload_resume(
        self,
        student_id: str,
        file,
    ) -> str:
        pass

    @abstractmethod
    def delete_resume(
        self,
        resume_path: str,
    ) -> None:
        pass

    @abstractmethod
    def get_resume_path(
        self,
        resume_path: str,
    ) -> str:
        pass