import io
import zipfile
from typing import Sequence, override

from judgelet.domain.files import Solution, File


class ZipSolution(Solution):
    """Represents a solution of multiple files."""

    def __init__(self, uid: str, bin_data: bytes, main_file: str):
        """Create zip container from binary data."""
        super().__init__(uid)
        self._bin = bin_data
        self._main_file = main_file
        self._files = []
        self._decompress()

    @override
    @property
    def files(self) -> Sequence[File]:
        return self._files

    @override
    @property
    def main_file_name(self) -> str | None:
        return self._main_file

    def _decompress(self):
        """Decompress virtually."""
        with io.BytesIO(self._bin) as b_io:
            zip_file = zipfile.ZipFile(b_io)
            for compressed_file in zip_file.namelist():
                with zip_file.open(compressed_file, "r") as zf_io:
                    self._files.append(File(
                        compressed_file,
                        zf_io.read().decode(),
                    ))
