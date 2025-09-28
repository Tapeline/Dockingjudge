from .conftest import (
    StrSolutionPoster,
    create_group,
    create_suite,
    create_test,
    create_validator,
)


def test_simple(post_str_solution: StrSolutionPoster):
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("stdout", expected="Hello, World!"),
                stdin=""
            )
        )
    )
    is_ok, result, response = post_str_solution(
        """
        print("Hello, World!")
        """,
        "python",
        test_suite
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_imports(post_str_solution: StrSolutionPoster):
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("stdout", expected="3.0"),
                stdin="-3"
            )
        )
    )
    is_ok, result, response = post_str_solution(
        """
        import math
        print(math.fabs(int(input())))
        """,
        "python",
        test_suite
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result
