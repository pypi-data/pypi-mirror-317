class NotYourType(Exception):
    def __init__(self, var):
        super().__init__(f"{var} must be string")


class PathNotExists(Exception):
    def __init__(self, path):
        super().__init__(f"Path {path} is not exists")


class NotGitHubUrl(Exception):
    def __init__(self, url):
        super().__init__(f"URL {url} is not follow the Github format")

class ChiveError(Exception):
    def __init__(self, message):
        super().__init__(message)
