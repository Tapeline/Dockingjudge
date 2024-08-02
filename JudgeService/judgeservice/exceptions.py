class ImproperlyConfiguredException(ValueError):
    pass


class NoJudgeletsSpecifiedException(ImproperlyConfiguredException):
    pass


class BadBalancingStrategy(ImproperlyConfiguredException):
    pass


class RequestProcessingException(Exception):
    CODE = "RPE"
    MESSAGE = "Request processing exception"

    def __init__(self, *args):
        super().__init__(self.MESSAGE % args)


class JudgeletNotFoundException(RequestProcessingException):
    CODE = "JUDGELET_NOT_FOUND"
    MESSAGE = "No available judgelet for compiler label %s"


class JudgeletAnswerException(RequestProcessingException):
    CODE = "JUDGELET_ANSWER_ERROR"
    MESSAGE = "Judgelet returned error %s"


class BadRequestFormatException(RequestProcessingException):
    CODE = "BAD_REQUEST"
    MESSAGE = "Request does not conform to valid format"
