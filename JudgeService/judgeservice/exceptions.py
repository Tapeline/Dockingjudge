class ImproperlyConfiguredException(ValueError):
    pass


class NoJudgeletsSpecifiedException(ImproperlyConfiguredException):
    pass


class BadBalancingStrategy(ImproperlyConfiguredException):
    pass
