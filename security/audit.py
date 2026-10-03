from datetime import datetime, timezone
from pathlib import Path
import json
import threading


class AuditLogger:
    def __init__(
        self,
        log_path: str,
        max_bytes: int = 1_000_000,
    ):
        if max_bytes <= 0:
            raise ValueError("max_bytes must be greater than zero.")

        self.log_path = Path(log_path)
        self.max_bytes = max_bytes
        self._lock = threading.Lock()

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _rotate_if_needed(self, entry_bytes: int) -> None:
        if not self.log_path.exists():
            return

        current_size = self.log_path.stat().st_size

        if current_size + entry_bytes <= self.max_bytes:
            return

        rotated = self.log_path.with_suffix(
            self.log_path.suffix + ".1"
        )

        if rotated.exists():
            rotated.unlink()

        self.log_path.replace(rotated)

    def record(
        self,
        event: str,
        action: str,
        status: str,
        details=None,
    ) -> None:

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "action": action,
            "status": status,
            "details": details or {},
        }

        line = (
            json.dumps(
                entry,
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n"
        )

        encoded = line.encode("utf-8")

        with self._lock:
            self._rotate_if_needed(len(encoded))

            with self.log_path.open(
                "a",
                encoding="utf-8",
            ) as handle:
                handle.write(line)
                handle.flush()
