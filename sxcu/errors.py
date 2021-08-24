class SubWrongToken(Exception):
    """Raise this error when the token seem wrong."""

    def __init__(self, message="The given token is not valid for the subdomain."):
        self.message = message
        super().__init__(self.message)


class SubNeedToken(Exception):
    """Raise this error when a token is needed."""

    def __init__(self, message="This domain require a token to allow image upload."):
        self.message = message
        super().__init__(self.message)


class UnallowedFileType(Exception):
    """Raise this error when the file is unallowed by API."""

    def __init__(self, message="The file type is not allowed for upload."):
        self.message = message
        super().__init__(self.message)


class APIRatelimited(Exception):
    """Raise this error when the API is ratelimiting the request."""

    def __init__(self, message="You are ratelimited."):
        self.message = message
        super().__init__(self.message)
