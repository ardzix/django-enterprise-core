from rest_framework.response import Response


class DRFResponse:
    def __init__(self, message):
        self.message = message

    def get_success_response(self, success_code, data, status=200):
        response_dict = {
            "status_code": str(self.status),
            "success_code": success_code,
            "message": self.message,
            "data": data,
        }
        return Response(response_dict, status=status)

    def get_error_response(self, error_code, data, status=400):
        response_dict = {
            "status_code": str(status),
            "error_code": error_code,
            "message": self.message,
            "data": data,
        }
        return Response(response_dict, status=status)
