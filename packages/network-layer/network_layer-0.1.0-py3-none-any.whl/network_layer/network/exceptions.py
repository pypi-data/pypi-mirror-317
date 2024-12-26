class NetworkError(Exception):
    pass


class ConnectionError(NetworkError):
    pass


class TimeoutError(NetworkError):
    pass


class AuthenticationError(NetworkError):
    pass


class RateLimitExceeded(NetworkError):
    pass
