import json
import tempfile
import unittest
from pathlib import Path

from security.audit import AuditLogger


class TestAuditLoggerHardening(unittest.TestCase):

    def test_rotation_keeps_log_bounded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"

            logger = AuditLogger(
                str(log_path),
                max_bytes=220,
            )

            for index in range(10):
                logger.record(
                    event="TEST",
                    action=f"action_{index}",
                    status="SUCCESS",
                    details={"index": index},
                )

            self.assertTrue(log_path.exists())
            self.assertTrue(
                log_path.stat().st_size <= 220
            )

            rotated = Path(
                str(log_path) + ".1"
            )

            self.assertTrue(rotated.exists())
            self.assertGreater(
                rotated.stat().st_size,
                0,
            )

    def test_invalid_max_bytes_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                AuditLogger(
                    str(Path(temp_dir) / "audit.jsonl"),
                    max_bytes=0,
                )

    def test_records_remain_valid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"

            logger = AuditLogger(
                str(log_path),
                max_bytes=10_000,
            )

            logger.record(
                event="TEST",
                action="unicode",
                status="SUCCESS",
                details={"message": "മലയാളം"},
            )

            entry = json.loads(
                log_path.read_text(
                    encoding="utf-8"
                ).splitlines()[0]
            )

            self.assertEqual(
                entry["event"],
                "TEST",
            )
            self.assertEqual(
                entry["details"]["message"],
                "മലയാളം",
            )

    def test_consecutive_records_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "audit.jsonl"

            logger = AuditLogger(
                str(log_path),
                max_bytes=10_000,
            )

            for index in range(20):
                logger.record(
                    event="TEST",
                    action=f"action_{index}",
                    status="SUCCESS",
                )

            entries = [
                json.loads(line)
                for line in log_path.read_text(
                    encoding="utf-8"
                ).splitlines()
            ]

            self.assertEqual(
                len(entries),
                20,
            )


if __name__ == "__main__":
    unittest.main()
