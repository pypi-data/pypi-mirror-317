class Error(Exception):
    """Clase base para los errores"""
    pass

class ResponseException(Error):
    """
    Clase para la definición de errores dentro de los microservicios
    """
    errorCode = 0
    message = ""
    headers = {}
    http_code = 0

    def __init__(self, error_code=-99, message='', http_status_code=None, headers={}):
        self.errorCode = error_code
        self.message = message
        self.headers = headers
        self.http_code = http_status_code
        super().__init__(self.errorCode)

    def to_dict(self):
        return {
            "status": self.http_code,
            "message": self.message,
            "code": self.errorCode,
            "headers": self.headers
        }