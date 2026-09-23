import tempfile
import unittest
from pathlib import Path

from files.authorization import (
    FileAuthorizer,
    FileAuthorizationError,
)
from files.chunker import TextChunker
from files.extractor import (
    FileExtractionError,
    TextExtractor,
)
from files.index import LocalTextIndex
from files.inspector import FileInspector
from files.models import (
    FileSupportStatus,
    FileType,
)
from files.service import FileService
from files.types import detect_file_type


class TestFilesFoundation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.root = Path(self.temp_dir.name)

        self.authorizer = FileAuthorizer([
            str(self.root)
        ])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_authorized_file(self):
        file_path = self.root / "notes.txt"
        file_path.write_text(
            "ANNA project note.",
            encoding="utf-8",
        )

        authorized = self.authorizer.require_authorized(
            str(file_path)
        )

        self.assertEqual(
            authorized,
            file_path.resolve(),
        )

    def test_unauthorized_file_rejected(self):
        outside = Path(self.temp_dir.name).parent / "outside.txt"

        with self.assertRaises(FileAuthorizationError):
            self.authorizer.require_authorized(
                str(outside)
            )

    def test_file_type_detection(self):
        file_type, status = detect_file_type(
            "example.py"
        )

        self.assertEqual(
            file_type,
            FileType.PY,
        )

        self.assertEqual(
            status,
            FileSupportStatus.SUPPORTED,
        )

    def test_optional_pdf_detection(self):
        file_type, status = detect_file_type(
            "example.pdf"
        )

        self.assertEqual(
            file_type,
            FileType.PDF,
        )

        self.assertEqual(
            status,
            FileSupportStatus.OPTIONAL,
        )

    def test_inspector(self):
        file_path = self.root / "notes.txt"
        file_path.write_text(
            "Hello ANNA.",
            encoding="utf-8",
        )

        inspector = FileInspector()

        metadata = inspector.inspect(
            str(file_path)
        )

        self.assertEqual(
            metadata.name,
            "notes.txt",
        )

        self.assertEqual(
            metadata.file_type,
            FileType.TXT,
        )

        self.assertEqual(
            metadata.support_status,
            FileSupportStatus.SUPPORTED,
        )

    def test_extractor(self):
        file_path = self.root / "notes.txt"
        file_path.write_text(
            "line one\nline two",
            encoding="utf-8",
        )

        metadata = FileInspector().inspect(
            str(file_path)
        )

        content = TextExtractor().extract(
            metadata
        )

        self.assertEqual(
            content,
            "line one\nline two",
        )

    def test_optional_format_extractor_rejected(self):
        file_path = self.root / "document.pdf"
        file_path.write_bytes(
            b"not a real pdf"
        )

        metadata = FileInspector().inspect(
            str(file_path)
        )

        with self.assertRaises(FileExtractionError):
            TextExtractor().extract(metadata)

    def test_chunker(self):
        content = "\n".join(
            f"line {number}"
            for number in range(1, 101)
        )

        chunker = TextChunker(
            max_lines=20,
            overlap_lines=5,
        )

        chunks = chunker.chunk(
            "example.txt",
            content,
        )

        self.assertGreater(
            len(chunks),
            1,
        )

        self.assertEqual(
            chunks[0].start_line,
            1,
        )

        self.assertEqual(
            chunks[0].end_line,
            20,
        )

    def test_index_search(self):
        index = LocalTextIndex()

        chunker = TextChunker()

        chunks = chunker.chunk(
            "python.txt",
            "Python variables are names that reference values.",
        )

        index.add(chunks)

        results = index.search(
            "Python variables",
            limit=5,
        )

        self.assertEqual(
            len(results),
            1,
        )

        self.assertGreater(
            results[0].score,
            0,
        )

    def test_file_service_ingest(self):
        file_path = self.root / "project.txt"

        file_path.write_text(
            "ANNA is a personal AI companion.\n"
            "ANNA also helps with learning.",
            encoding="utf-8",
        )

        service = FileService(
            authorizer=self.authorizer
        )

        metadata, chunks = service.ingest(
            str(file_path)
        )

        self.assertEqual(
            metadata.file_type,
            FileType.TXT,
        )

        self.assertGreaterEqual(
            len(chunks),
            1,
        )

        results = service.search(
            "personal AI companion"
        )

        self.assertGreaterEqual(
            len(results),
            1,
        )


if __name__ == "__main__":
    unittest.main()
