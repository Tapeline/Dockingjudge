import pytest

from api.validation import TestSuite
from tests.common import api, create_client, create_contest


@pytest.fixture
def dummy_test_suite():
    return TestSuite(
        place_files={},
        precompile=[],
        groups=[],
        public_cases=[],
        time_limit=1,
        mem_limit_mb=256,
        compile_timeout=5,
    ).model_dump()


@pytest.fixture
def populated_contest(client, contest, dummy_test_suite):
    """A contest with one of each page type."""
    text_res = client.post(
        api(f"{contest.id}/tasks/text/"),
        {"name": "Intro", "text": "Welcome"},
        format="json",
    )
    quiz_res = client.post(
        api(f"{contest.id}/tasks/quiz/"),
        {
            "title": "Quiz 1",
            "description": "...",
            "validator": {"type": "text", "args": {"pattern": "..."}},
            "points": 10,
        },
        format="json",
    )
    code_res = client.post(
        api(f"{contest.id}/tasks/code/"),
        {
            "title": "Code 1",
            "description": "...",
            "test_suite": dummy_test_suite,
        },
        format="json",
    )
    return {
        "contest": contest,
        "text_id": text_res.data["id"],
        "quiz_id": quiz_res.data["id"],
        "code_id": code_res.data["id"],
    }


@pytest.fixture
def client(author):
    """Authenticated client for the contest author."""
    return create_client(author.token)


@pytest.fixture
def contest(author):
    """A contest created by the author."""
    return create_contest(author.id)
