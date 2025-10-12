class ImproperlyConfiguredException(ValueError):
    """Raised when judge service is improperly configured."""


class BadBalancingStrategy(ImproperlyConfiguredException):
    """Raised when a balancing strategy is invalid."""
