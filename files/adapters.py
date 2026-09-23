from dataclasses import dataclass


@dataclass(frozen=True)
class OptionalAdapter:
    file_type: str
    package: str
    installed: bool


class AdapterRegistry:

    def __init__(self):
        self._adapters = {}

    def register(
        self,
        file_type: str,
        package: str,
        installed: bool,
    ) -> None:

        self._adapters[file_type] = OptionalAdapter(
            file_type=file_type,
            package=package,
            installed=installed,
        )

    def get(self, file_type: str):
        return self._adapters.get(file_type)

    def all(self) -> list[OptionalAdapter]:
        return list(self._adapters.values())
