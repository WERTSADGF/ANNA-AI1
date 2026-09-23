from pathlib import Path


class FileAuthorizationError(PermissionError):
    pass


class FileAuthorizer:

    def __init__(self, allowed_directories: list[str]):
        self.allowed_directories = [
            Path(directory).resolve()
            for directory in allowed_directories
        ]

    def is_authorized(self, path: str) -> bool:
        target = Path(path).resolve()

        for allowed in self.allowed_directories:
            if target == allowed:
                return True

            if allowed in target.parents:
                return True

        return False

    def require_authorized(self, path: str) -> Path:
        resolved = Path(path).resolve()

        if not self.is_authorized(str(resolved)):
            raise FileAuthorizationError(
                f"File is outside authorized directories: {resolved}"
            )

        return resolved
