import requests

from tests.integration.api_connection import api_url
from tests.integration.fixtures import (TestSuiteDataFactory,
                                        create_group_with_stdout_validation,
                                        test_suite_data_factory,
                                        StdoutValidationCase)


def test_ok_with_python_code(test_suite_data_factory: TestSuiteDataFactory):
    test_suite = test_suite_data_factory(
        "python",
        "print(int(input()) * 2)",
        [create_group_with_stdout_validation("A", [
            StdoutValidationCase(stdin="3\n", stdout="6"),
            StdoutValidationCase(stdin="0\n", stdout="0")
        ])]
    )
    response = requests.post(api_url("run-suite"), data=test_suite.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["score"] == 100
    assert response_json["verdict"] == "OK"


def test_wa_with_python_code(test_suite_data_factory: TestSuiteDataFactory):
    test_suite = test_suite_data_factory(
        "python",
        "print(int(input()) ** 2)",
        [create_group_with_stdout_validation("A", [
            StdoutValidationCase(stdin="2\n", stdout="4"),
            StdoutValidationCase(stdin="3\n", stdout="6")
        ])]
    )
    response = requests.post(api_url("run-suite"), data=test_suite.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["score"] == 50
    assert response_json["verdict"] == "WA"


def test_tl_with_python_code(test_suite_data_factory: TestSuiteDataFactory):
    test_suite = test_suite_data_factory(
        "python",
        "while True: print('')",
        [create_group_with_stdout_validation("A", [
            StdoutValidationCase(stdin="2\n", stdout="4"),
            StdoutValidationCase(stdin="3\n", stdout="6")
        ])]
    )
    response = requests.post(api_url("run-suite"), data=test_suite.json())
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["score"] == 0
    assert response_json["verdict"] == "TL"
