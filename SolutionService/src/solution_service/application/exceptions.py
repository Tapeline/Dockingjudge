class NotFound(Exception):
    """Raised when an object is not found."""


class MayNotAccessSolution(Exception):
    """Raised when you cannot access a solution."""


class NotAuthenticated(Exception):
    """Raised when you did not provide credentials."""
