from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage

from app.services.storage.storage_service import StorageService


class LocalStorageService(StorageService):

    UPLOAD_DIRECTORY = Path(current_app.config["UPLOAD_DIRECTORY"])

    def __init__(self):
        self.UPLOAD_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload_resume(
        self,
        student_id: str,
        file: FileStorage,
    ) -> str:

        filename = f"{student_id}.pdf"

        destination = self.UPLOAD_DIRECTORY / filename

        file.save(destination)

        return str(destination)

    def delete_resume(
        self,
        resume_path: str,
    ) -> None:

        path = Path(resume_path)

        if path.exists():
            path.unlink()

    def get_resume_path(
        self,
        resume_path: str,
    ) -> str:
        return resume_path