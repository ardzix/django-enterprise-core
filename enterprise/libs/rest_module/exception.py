from rest_framework.exceptions import APIException


class ErrorValidationException(APIException):
    default_code = "invalid"
    status_code = 400

    def __init__(self, error_code, message, data, status_code=400):
        if message is None:
            message = self.detail
        if status_code is None:
            status_code = self.default_code

        self.status_code = status_code
        self.detail = self.response_message(error_code, message, data, status_code)

    def response_message(self, error_code, message, data, status_code):
        response_dict = {
            "status_code": status_code,
            "error_code": error_code,
            "message": message,
            "data": data,
        }

        return response_dict
