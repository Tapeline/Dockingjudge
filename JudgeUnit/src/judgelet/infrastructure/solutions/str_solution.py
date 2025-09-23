from typing import Sequence

from judgelet.domain.files import Solution, File


class StringSolution(Solution):
    def __init__(self, uid: str, filename: str, content: str) -> None:
        super().__init__(uid)
        self.filename = filename
        self.content = content

    @property
    def files(self) -> Sequence[File]:
        return [
            File(self.filename, self.content)
        ]

    @property
    def main_file_name(self) -> str | None:
        return self.filename
