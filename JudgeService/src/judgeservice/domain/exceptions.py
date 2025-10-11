"""Contains domain exceptions."""


class NoSuitableJudgeletFoundException(Exception):
    """Raised when no judgelet for a compiler found."""


class BadJudgeletResponseException(Exception):
    """Raised when judgelet returns non-OK code."""
