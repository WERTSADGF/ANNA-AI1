from pathlib import Path

from files.models import FileMetadata, FileSupportStatus


class FileExtractionError(RuntimeError):
    pass


class TextExtractor:

    ENCODINGS = (
        "utf-8-sig",
        "utf-8",
        "utf-16",
        "latin-1",
    )

    def extract(
        self,
        metadata: FileMetadata,
    ) -> str:

        if metadata.support_status != FileSupportStatus.SUPPORTED:
            raise FileExtractionError(
                f"No built-in extractor for file type: "
                f"{metadata.file_type.value}"
            )

        path = Path(metadata.path)

        raw = path.read_bytes()

        for encoding in self.ENCODINGS:
            try:
                text = raw.decode(encoding)

                # Normalize Windows CRLF and legacy CR line endings
                # so extracted text has one consistent representation.
                return text.replace("\r\n", "\n").replace("\r", "\n")

            except UnicodeDecodeError:
                continue

        raise FileExtractionError(
            f"Could not decode file: {metadata.path}"
        )
