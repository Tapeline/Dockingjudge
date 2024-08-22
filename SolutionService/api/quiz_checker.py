import re
from abc import ABC, abstractmethod


class AbstractQuizValidator(ABC):
    @abstractmethod
    def validate(self, data: str, pattern: str) -> bool:
        raise NotImplementedError


class RegexQuizValidator(AbstractQuizValidator):
    def validate(self, data: str, pattern: str) -> bool:
        return re.fullmatch(pattern, data) is not None


class ContainsStrQuizValidator(AbstractQuizValidator):
    def validate(self, data: str, pattern: str) -> bool:
        return pattern in data


def create_validator(validator_type: str):
    if validator_type == "regex":
        return RegexQuizValidator()
    if validator_type == "contains":
        return ContainsStrQuizValidator()
