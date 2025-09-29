import os
import textwrap
import uuid
from collections.abc import Callable
from typing import Any

import pytest
import requests

from judgelet.controllers.schemas.response import RunResponse
from tests.integration.conftest import create_zip_archive, to_base64

SolutionPosterReturn = tuple[bool, RunResponse | dict, requests.Response]
StrSolutionPoster = Callable[
    [str, str, Any],
    SolutionPosterReturn,
]
ZipSolutionPoster = Callable[
    [dict[str, str], str, str, Any],
    SolutionPosterReturn,
]
AnySolutionPoster = StrSolutionPoster | ZipSolutionPoster

JUDGELET_URL = os.environ.get("JUDGELET_URL", "http://localhost:9090")


@pytest.fixture
def post_str_solution() -> StrSolutionPoster:
    def post(
        source: str,
        compiler_name: str,
        test_suite: Any,
    ) -> SolutionPosterReturn:
        uid = uuid.uuid4()
        response = requests.post(
            url=f"{JUDGELET_URL}/run",
            json={
                "id": str(uid),
                "code": {
                    "type": "str",
                    "code": textwrap.dedent(source),
                },
                "compiler": compiler_name,
                "suite": test_suite,
            },
            timeout=5,
        )
        if response.status_code != 201:
            return False, response.text, response
        return True, RunResponse.model_validate(response.json()), response

    return post


@pytest.fixture
def post_zip_solution() -> ZipSolutionPoster:
    def post(
        files: dict[str, str],
        main_file: str,
        compiler_name: str,
        test_suite: Any,
    ) -> SolutionPosterReturn:
        uid = uuid.uuid4()
        zip_bytes = create_zip_archive(
            {
                filename: textwrap.dedent(file_content)
                for filename, file_content in files.items()
            },
        )
        response = requests.post(
            url=f"{JUDGELET_URL}/run",
            json={
                "id": str(uid),
                "code": {
                    "type": "zip",
                    "b64": to_base64(zip_bytes),
                    "main": main_file,
                },
                "compiler": compiler_name,
                "suite": test_suite,
            },
            timeout=5,
        )
        if response.status_code != 201:
            return False, response.text, response
        return True, RunResponse.model_validate(response.json()), response

    return post


def create_suite(
    *groups,
    precompile_checks=None,
    additional_files: dict[str, str] | None = None,
    default_time_limit: int = 1,
    default_mem_limit: int = 256,
    compile_timeout: int = 5,
    envs: dict[str, str] | None = None,
):
    return {
        "groups": groups,
        "precompile": precompile_checks or [],
        "time_limit": default_time_limit,
        "mem_limit_mb": default_mem_limit,
        "compile_timeout": compile_timeout,
        "place_files": additional_files or {},
        "public_cases": [],
        "envs": envs or {},
    }


def create_group(
    name: str,
    *cases,
    depends_on: list[str] | None = None,
    score: int = 100,
    scoring_policy: str = "graded",
):
    return {
        "name": name,
        "depends_on": depends_on or [],
        "points": score,
        "scoring_rule": scoring_policy,
        "cases": cases,
    }


def create_test(
    *validators,
    stdin: str,
    time_limit: int = 1,
    mem_limit: int = 256,
    input_files: dict[str, str] | None = None,
    output_files: list[str] | None = None,
):
    return {
        "validators": validators,
        "stdin": stdin,
        "files_in": input_files or {},
        "files_out": output_files or [],
        "time_limit": time_limit,
        "mem_limit_mb": mem_limit,
    }


def create_validator(validator_type: str, **v_args):
    return {
        "type": validator_type,
        "args": v_args,
    }
