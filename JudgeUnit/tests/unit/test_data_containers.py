import base64
import os
import shutil
from pathlib import Path

import pytest

from judgelet.data.container import SolutionContainer, place_all_solution_files


@pytest.fixture()
def dir_test_data_container():
    Path("_test_data_container").mkdir(exist_ok=True)
    yield "_test_data_container"
    shutil.rmtree("_test_data_container")


def test_string_container(dir_test_data_container):
    container = SolutionContainer.from_json({
        "type": "string",
        "name": "main.py",
        "code": "print('Hello, World!')"
    })
    place_all_solution_files(container, "_test_data_container")
    assert set(os.listdir("_test_data_container")) == {"main.py"}
    assert Path("_test_data_container/main.py").read_text() == "print('Hello, World!')"


def test_zip_container(dir_test_data_container):
    Path(dir_test_data_container).mkdir(exist_ok=True)
    Path(f"{dir_test_data_container}/main.py").write_text("print('Hello, World!')")
    Path(f"{dir_test_data_container}/test.py").write_text("# This is a dummy file")
    shutil.make_archive(f"{dir_test_data_container}/data", "zip", dir_test_data_container)
    os.remove(f"{dir_test_data_container}/main.py")
    os.remove(f"{dir_test_data_container}/test.py")

    container = SolutionContainer.from_json({
        "type": "zip",
        "main": "main.py",
        "b64": base64.b64encode(Path(f"{dir_test_data_container}/data.zip").read_bytes()).decode()
    })
    place_all_solution_files(container, dir_test_data_container)

    assert set(os.listdir(dir_test_data_container)) == {"main.py", "test.py", "data.zip"}
    assert Path(f"{dir_test_data_container}/main.py").read_text() == "print('Hello, World!')"
    assert Path(f"{dir_test_data_container}/test.py").read_text() == "# This is a dummy file"
