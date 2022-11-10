from ninja.errors import AuthenticationError 


class ApiAuthError(AuthenticationError): 
    def __init__(self, message, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.message = message

    def __str__(self): 
        return self.message
