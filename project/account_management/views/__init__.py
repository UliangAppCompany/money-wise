import ninja


class ErrorMessageSchema(ninja.Schema):
    message: str


class SupercategoryUnavailableError(Exception):
    pass


class DuplicateValueError(Exception):
    pass
