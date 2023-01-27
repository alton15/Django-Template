from rest_framework.response import Response


class GeneralResponse:
    """ GeneralResponse Class
    General definition of API Response
    """

    def __init__(self, status_code, message, payload):
        """
        Params:
            code: HTTP status code
            message: Response message
            payload: Response data
        """
        self.response = {
            'code': status_code,
            'message': message,
            'payload': payload
        }

    def __repr__(self):
        return repr(self.response)


# TODO: 프로젝트의 이름에 따라 Response class (NamedServer_Response) 의 이름 변경 필요
class NamedServer_Response(Response):
    def __init__(self, status_code, message, payload):
        super().__init__(
            status=status_code,
            data=GeneralResponse(status_code, message, payload).response
        )
