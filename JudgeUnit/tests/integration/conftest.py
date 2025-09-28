import base64
import io
import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path

import pytest


def create_zip_archive(files: dict[str, str]) -> bytes:
    b_io = io.BytesIO()
    with zipfile.ZipFile(b_io, "w") as zip_file:
        for filename, file_content in files.items():
            zip_file.writestr(filename, file_content.encode())
    return b_io.getvalue()


def to_base64(b_data: bytes) -> str:
    return base64.b64encode(b_data).decode()


def from_base64(b64_data: str) -> bytes:
    return base64.b64decode(b64_data)


@pytest.fixture()
def dir_test_data_container():
    unique_postfix = hex(hash(uuid.uuid4()))[2:]
    dirname = f"_test_data_container_{unique_postfix}"
    Path(dirname).mkdir()
    yield dirname
    shutil.rmtree(dirname)
