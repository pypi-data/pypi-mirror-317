class BizError(RuntimeError):
    def __init__(self, code, message):
        super().__init__(code, message)

    @property
    def code(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]


class BadReqeust(BizError):
    def __init__(self, code=400, message="Bad Reqeust"):
        super().__init__(code, message)


class RequestValidationError(BadReqeust):
    def __init__(self, code=400, message="Validation Error"):
        super().__init__(code, message)


class Forbidden(BizError):
    def __init__(self, code=403, message="Forbidden"):
        super().__init__(code, message)


class MethodNotAllowed(BizError):
    def __init__(self, code=405, message="Method Not Allowed"):
        super().__init__(code, message)


class UnsupportedMediaType(BizError):
    def __init__(self, code=415, message="Unsupported Media Type"):
        super().__init__(code, message)


class InternalServerError(BizError):
    def __init__(self, code=500, message="Internal Server Error"):
        super().__init__(code, message)
