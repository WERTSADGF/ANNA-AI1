from dataclasses import dataclass
from enum import Enum


class FileType(str, Enum):
    TXT = "txt"
    MD = "md"
    PY = "py"
    JS = "js"
    TS = "ts"
    JSX = "jsx"
    TSX = "tsx"
    HTML = "html"
    CSS = "css"
    JSON = "json"
    CSV = "csv"
    YAML = "yaml"
    YML = "yml"
    XML = "xml"
    LOG = "log"
    SQL = "sql"
    PS1 = "ps1"
    BAT = "bat"
    CMD = "cmd"
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    XLSX = "xlsx"
    IMAGE = "image"
    UNKNOWN = "unknown"


class FileSupportStatus(str, Enum):
    SUPPORTED = "supported"
    OPTIONAL = "optional"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True)
class FileMetadata:
    path: str
    name: str
    extension: str
    size_bytes: int
    modified_at: float
    file_type: FileType
    support_status: FileSupportStatus


@dataclass(frozen=True)
class FileChunk:
    chunk_id: str
    file_path: str
    index: int
    content: str
    start_line: int
    end_line: int
    source_hash: str


@dataclass(frozen=True)
class FileSearchResult:
    chunk: FileChunk
    score: float
