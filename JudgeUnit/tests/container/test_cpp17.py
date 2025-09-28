from .conftest import (
    StrSolutionPoster,
    ZipSolutionPoster,
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
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """,
        "cpp17",
        test_suite
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result


def test_imports(post_zip_solution: ZipSolutionPoster):
    test_suite = create_suite(
        create_group(
            "A",
            create_test(
                create_validator("stdout", expected="Hello, World!"),
                stdin=""
            )
        )
    )
    is_ok, result, response = post_zip_solution(
        {
            "main.cpp":
                """
                #include "hello_world.h"
                #include <iostream>
                int main() {
                    SAY("Hello, World!");
                    return 0;
                }
                """,
            "hello_world.h":
                """
                #define SAY(something) std::cout << something << std::endl
                """
        },
        "main.cpp",
        "cpp17",
        test_suite
    )
    assert is_ok, result
    assert result.verdict == "OK", result
    assert result.score == 100, result
