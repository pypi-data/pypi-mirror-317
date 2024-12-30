__all__ = [
    "SteampieException",
    "SevenDaysHoldException",
    "TooManyRequests",
    "ApiException",
    "LoginRequired",
    "InvalidCredentials",
    "CaptchaRequired",
    "ConfirmationExpected",
    "ProxyConnectionError",
]


class SteampieException(Exception):
    pass


class SevenDaysHoldException(SteampieException):
    pass


class TooManyRequests(SteampieException):
    pass


class ApiException(SteampieException):
    pass


class LoginRequired(SteampieException):
    pass


class InvalidCredentials(SteampieException):
    pass


class CaptchaRequired(SteampieException):
    pass


class ConfirmationExpected(SteampieException):
    pass


class ProxyConnectionError(SteampieException):
    pass
