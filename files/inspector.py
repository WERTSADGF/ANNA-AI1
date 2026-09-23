from pathlib import Path

from files.models import FileMetadata
from files.types import detect_file_type


class FileInspector:

    def inspect(self, path: str) -> FileMetadata:

        file_path = Path(path).resolve()

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Path is not a file: {file_path}"
            )

        file_type, support_status = detect_file_type(
            str(file_path)
        )

        stat = file_path.stat()

        return FileMetadata(
            path=str(file_path),
            name=file_path.name,
            extension=file_path.suffix.lower(),
            size_bytes=stat.st_size,
            modified_at=stat.st_mtime,
            file_type=file_type,
            support_status=support_status,
        )
