from .conftest import (
    StrSolutionPoster,
    ZipSolutionPoster,
    create_group,
    create_suite,
    create_test,
    create_validator,
)


def test_stdio(post_str_solution: StrSolutionPoster):
    """Test that stdin/stdout works."""
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("stdout", expected="9"),
                stdin="3",
            ),
        ),
    )
    is_ok, result, _ = post_str_solution(
        """
        print(int(input())**2)
        """,
        "python",
        test_suite,
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_file_io(post_str_solution: StrSolutionPoster):
    """Test that files can be read and written."""
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("file", filename="out", expected="9"),
                stdin="",
                input_files={"in": "3"},
                output_files=["out"],
            ),
        ),
    )
    is_ok, result, _ = post_str_solution(
        """
        with (
            open("in", "r") as fin,
            open("out", "w") as fout
        ):
            fout.write(str(int(fin.read().strip()) ** 2))
        """,
        "python",
        test_suite,
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_additional_files(post_str_solution: StrSolutionPoster):
    """Test that additional files are placed."""
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator(
                    "file", filename="per_test", expected="content 1",
                ),
                create_validator(
                    "file", filename="additional", expected="content 2",
                ),
                stdin="",
                input_files={"per_test": "content 1"},
                output_files=["additional", "per_test"],
            ),
        ),
        additional_files={
            "additional": "content 2",
        },
    )
    is_ok, result, _ = post_str_solution(
        "",
        "python",
        test_suite,
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_envs(post_str_solution: StrSolutionPoster):
    """Test that envs are placed and could be read."""
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("stdout", expected="env_value"),
                stdin="",
            ),
        ),
        envs={"TEST_ENV": "env_value"},
    )
    is_ok, result, _ = post_str_solution(
        """
        import os
        print(os.environ.get("TEST_ENV"))
        """,
        "python",
        test_suite,
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_zip_solution(post_zip_solution: ZipSolutionPoster):
    """Test that zip solution unpacks and works well."""
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator(
                    "file", filename="other_file", expected="test",
                ),
                stdin="",
                output_files=["other_file"],
            ),
        ),
    )
    is_ok, result, _ = post_zip_solution(
        {
            "main.py": "",
            "other_file": "test",
        },
        "main.py",
        "python",
        test_suite,
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result
