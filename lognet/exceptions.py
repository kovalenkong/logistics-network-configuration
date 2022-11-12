class NetworkException(Exception):
    pass


class UnsupportedFileExtension(NetworkException):
    pass


class NoSolution(NetworkException):
    pass
