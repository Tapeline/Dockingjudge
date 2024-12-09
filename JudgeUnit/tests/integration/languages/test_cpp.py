import requests

from tests.integration.api_connection import api_url
from tests.integration.fixtures import (TestSuiteDataFactory,
                                        create_group_with_stdout_validation,
                                        test_suite_data_factory,
                                        StdoutValidationCase)


def test_ok_with_cpp_code(test_suite_data_factory: TestSuiteDataFactory):
    test_suite = test_suite_data_factory(
        "cpp",
        """
        #include <iostream>
        int main() {
            int n;
            std::cin >> n;
            std::cout << 1ll * n * n << std::endl;
            return 0;
        }
        """,
        [create_group_with_stdout_validation("A", [
            StdoutValidationCase(stdin="3\n", stdout="9"),
            StdoutValidationCase(stdin="0\n", stdout="0"),
            StdoutValidationCase(stdin="1\n", stdout="1"),
            StdoutValidationCase(stdin="10\n", stdout="100"),
        ])]
    )
    response = requests.post(api_url("run-suite"), data=test_suite.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["score"] == 100
    assert response_json["verdict"] == "OK"


def test_ce_with_cpp_code(test_suite_data_factory: TestSuiteDataFactory):
    test_suite = test_suite_data_factory(
        "cpp",
        """
        #include <invalid library>
        """,
        [create_group_with_stdout_validation("A", [])]
    )
    response = requests.post(api_url("run-suite"), data=test_suite.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["score"] == 0
    assert response_json["verdict"] == "CE"
