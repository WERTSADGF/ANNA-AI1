from pathlib import Path


class DirectoryAllowlist:
    def __init__(self, allowed_directories=None):
        self._allowed = [
            Path(directory).resolve()
            for directory in (allowed_directories or [])
        ]

    def is_allowed(self, path: str) -> bool:
        target = Path(path).resolve()

        for allowed in self._allowed:
            if target == allowed:
                return True

            if allowed in target.parents:
                return True

        return False
