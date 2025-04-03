import os
import shutil
from pathlib import Path

from judgelet.domain.files import FileSystem, File, Solution


class FileSystemImpl(FileSystem):
    def __init__(self, root: str = "solutions") -> None:
        self.root = root
        self.solution = None
        self._ensure_root_exists()

    def place_solution(self, solution: Solution) -> Path:
        root = self._solution_root(solution.uid)
        if root.exists():
            delete(root)
        root.mkdir(parents=True)
        self.solution = solution
        for solution_file in solution.files:
            self.save_file(solution_file)
        return root

    def cleanup(self, solution: Solution) -> None:
        delete(self._solution_root(solution.uid))
        self.solution = None

    def get_file(self, path: str) -> File | None:
        file_path = Path(self._solution_root(self.solution.uid), path)
        if not file_path.exists():
            return None
        return File(path, file_path.read_text())

    def save_file(self, file: File) -> None:
        file_path = Path(self._solution_root(self.solution.uid), file.name)
        file_path.write_text(file.contents)

    def delete_file(self, filename: str) -> None:
        file_path = Path(self._solution_root(self.solution.uid), filename)
        delete(file_path)

    def _ensure_root_exists(self) -> None:
        Path(self.root).mkdir(exist_ok=True, parents=True)

    def _solution_root(self, uid: str) -> Path:
        return Path(self.root, f"s_{uid}")


def delete(path: Path):
    if path.is_dir():
        shutil.rmtree(path)
    else:
        os.remove(path)
