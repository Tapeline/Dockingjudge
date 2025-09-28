import os
from pathlib import Path

import pytest

from judgelet.domain.files import File
from judgelet.infrastructure.filesystem import RealFileSystem
from judgelet.infrastructure.solutions.str_solution import StringSolution
from judgelet.infrastructure.solutions.zip_solution import ZipSolution
from .conftest import create_zip_archive


@pytest.mark.parametrize(
    "src",
    [
        "",
        "print('Hello, World!')"
    ]
)
@pytest.mark.parametrize(
    "filename",
    ["main.py"]
)
def test_str_container(
    dir_test_data_container: str,
    filename: str,
    src: str
):
    real_fs = RealFileSystem(dir_test_data_container)

    solution = StringSolution(uid="1", filename=filename, content=src)
    solution_path = real_fs.place_solution(solution)

    assert set(os.listdir(str(solution_path))) == {filename}
    assert Path(solution_path, filename).read_text() == src

    # This is kind of an unrelated assert, but I don't know where to put it.
    # Should move away, but for now, let it stay here
    assert solution.main_file == File(filename, src)



@pytest.mark.parametrize(
    "archive_data",
    [
        {"main.py": ""},
        {"main.py": "print('Hello, World!')"},
        {"main.py": "some code", "test.py": "some code 2"}
    ]
)
def test_zip_container(
    dir_test_data_container: str,
    archive_data: dict[str, str],
):
    main_file = "main.py"
    zip_data = create_zip_archive(archive_data)
    real_fs = RealFileSystem(dir_test_data_container)

    solution = ZipSolution(uid="1", bin_data=zip_data, main_file=main_file)
    solution_path = real_fs.place_solution(solution)

    assert set(os.listdir(str(solution_path))) == archive_data.keys()

    for filename, file_contents in archive_data.items():
        assert Path(
            solution_path, filename
        ).read_text() == file_contents

    # This is kind of an unrelated assert, but I don't know where to put it.
    # Should move away, but for now, let it stay here
    assert solution.main_file == File(main_file, archive_data[main_file])
