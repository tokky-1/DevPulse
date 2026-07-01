class DevPulseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UserNotFoundException(DevPulseException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class GitHubAPIException(DevPulseException):
    def __init__(self, message: str):
        super().__init__(message)


class SyncException(DevPulseException):
    def __init__(self, message: str):
        super().__init__(message)