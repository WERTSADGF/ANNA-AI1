from hashlib import sha256
from uuid import uuid4

from files.models import FileChunk


class TextChunker:

    def __init__(
        self,
        max_lines: int = 40,
        overlap_lines: int = 5,
    ):
        if max_lines <= 0:
            raise ValueError("max_lines must be positive.")

        if overlap_lines < 0:
            raise ValueError("overlap_lines cannot be negative.")

        if overlap_lines >= max_lines:
            raise ValueError(
                "overlap_lines must be smaller than max_lines."
            )

        self.max_lines = max_lines
        self.overlap_lines = overlap_lines

    def chunk(
        self,
        file_path: str,
        content: str,
    ) -> list[FileChunk]:

        lines = content.splitlines()

        if not lines:
            return []

        source_hash = sha256(
            content.encode("utf-8")
        ).hexdigest()

        chunks = []

        start = 0
        index = 0

        step = self.max_lines - self.overlap_lines

        while start < len(lines):

            end = min(
                start + self.max_lines,
                len(lines),
            )

            chunk_content = "\n".join(
                lines[start:end]
            )

            chunks.append(
                FileChunk(
                    chunk_id=str(uuid4()),
                    file_path=file_path,
                    index=index,
                    content=chunk_content,
                    start_line=start + 1,
                    end_line=end,
                    source_hash=source_hash,
                )
            )

            if end >= len(lines):
                break

            start += step
            index += 1

        return chunks
