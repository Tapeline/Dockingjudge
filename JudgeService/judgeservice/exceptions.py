class ImproperlyConfiguredException(ValueError):
    pass


class NoJudgeletsSpecifiedException(ImproperlyConfiguredException):
    pass


class BadBalancingStrategy(ImproperlyConfiguredException):
    pass


class RequestProcessingException(Exception):
    pass


class JudgeletNotFoundException(RequestProcessingException):
    pass


class JudgeletAnswerException(RequestProcessingException):
    pass


class BadRequestFormatException(RequestProcessingException):
    pass
