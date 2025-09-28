from collections.abc import Sequence
from typing import override

from judgelet.domain.files import File, Solution


class StringSolution(Solution):
    """Represents a simple solution - a single source string."""

    def __init__(self, uid: str, filename: str, content: str) -> None:
        super().__init__(uid)
        self.filename = filename
        self.content = content

    @override
    @property
    def files(self) -> Sequence[File]:
        return [
            File(self.filename, self.content),
        ]

    @override
    @property
    def main_file_name(self) -> str | None:
        return self.filename
