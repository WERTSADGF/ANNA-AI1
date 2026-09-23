from pathlib import Path

from files.models import FileSupportStatus, FileType


SUPPORTED_EXTENSIONS = {
    ".txt": (FileType.TXT, FileSupportStatus.SUPPORTED),
    ".md": (FileType.MD, FileSupportStatus.SUPPORTED),
    ".py": (FileType.PY, FileSupportStatus.SUPPORTED),
    ".js": (FileType.JS, FileSupportStatus.SUPPORTED),
    ".ts": (FileType.TS, FileSupportStatus.SUPPORTED),
    ".jsx": (FileType.JSX, FileSupportStatus.SUPPORTED),
    ".tsx": (FileType.TSX, FileSupportStatus.SUPPORTED),
    ".html": (FileType.HTML, FileSupportStatus.SUPPORTED),
    ".css": (FileType.CSS, FileSupportStatus.SUPPORTED),
    ".json": (FileType.JSON, FileSupportStatus.SUPPORTED),
    ".csv": (FileType.CSV, FileSupportStatus.SUPPORTED),
    ".yaml": (FileType.YAML, FileSupportStatus.SUPPORTED),
    ".yml": (FileType.YML, FileSupportStatus.SUPPORTED),
    ".xml": (FileType.XML, FileSupportStatus.SUPPORTED),
    ".log": (FileType.LOG, FileSupportStatus.SUPPORTED),
    ".sql": (FileType.SQL, FileSupportStatus.SUPPORTED),
    ".ps1": (FileType.PS1, FileSupportStatus.SUPPORTED),
    ".bat": (FileType.BAT, FileSupportStatus.SUPPORTED),
    ".cmd": (FileType.CMD, FileSupportStatus.SUPPORTED),

    ".pdf": (FileType.PDF, FileSupportStatus.OPTIONAL),
    ".docx": (FileType.DOCX, FileSupportStatus.OPTIONAL),
    ".pptx": (FileType.PPTX, FileSupportStatus.OPTIONAL),
    ".xlsx": (FileType.XLSX, FileSupportStatus.OPTIONAL),

    ".png": (FileType.IMAGE, FileSupportStatus.OPTIONAL),
    ".jpg": (FileType.IMAGE, FileSupportStatus.OPTIONAL),
    ".jpeg": (FileType.IMAGE, FileSupportStatus.OPTIONAL),
    ".webp": (FileType.IMAGE, FileSupportStatus.OPTIONAL),
}


def detect_file_type(path: str) -> tuple[FileType, FileSupportStatus]:
    extension = Path(path).suffix.lower()

    return SUPPORTED_EXTENSIONS.get(
        extension,
        (FileType.UNKNOWN, FileSupportStatus.UNSUPPORTED),
    )
