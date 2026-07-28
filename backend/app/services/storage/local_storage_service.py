from pathlib import Path

from flask import current_app
from werkzeug.datastructures import FileStorage

from app.services.storage.storage_service import StorageService


class LocalStorageService(StorageService):

    def upload_resume(
        self,
        student_id: str,
        file: FileStorage,
    ) -> str:

        upload_directory = Path(current_app.config["UPLOAD_DIRECTORY"])

        upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = f"{student_id}.pdf"

        destination = upload_directory / filename

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