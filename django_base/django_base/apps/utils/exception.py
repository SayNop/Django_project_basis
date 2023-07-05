from rest_framework.views import Response
from rest_framework.views import exception_handler

from .response_code import FRAMEWORK, PARAMS_INVALID


# exception response pass into Renderer, can change data format again in Renderer class
def custom_exception_handler(exc, context):
    # get standard exception obj
    response = exception_handler(exc, context)

    data = dict(success=False)
    if response is not None:
        for index, value in enumerate(response.data):
            if index == 0:
                key = value
                value = response.data[key]

                # put error message in response data
                if isinstance(value, str):
                    # detail str
                    data['code'] = FRAMEWORK
                    data['message'] = value

                elif isinstance(value, list):
                    # params parse fail
                    data['code'] = PARAMS_INVALID
                    data['message'] = key + value[0]

                else:
                    # other situation
                    data['code'] = FRAMEWORK
                    data['message'] = str(value)
                # return custom data
                return Response(data, status=response.status_code, exception=True)

    return response
