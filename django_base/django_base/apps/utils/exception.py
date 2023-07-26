from rest_framework.views import Response
from rest_framework.views import exception_handler

from .response import response_format, FRAMEWORK, PARAMS_INVALID


# exception response pass into Renderer, can change data format again in Renderer class
def custom_exception_handler(exc, context):
    # get standard exception obj
    response = exception_handler(exc, context)

    if response is not None:
        for index, value in enumerate(response.data):
            if index == 0:
                key = value
                value = response.data[key]

                # put error message in response data
                if isinstance(value, str):
                    # detail str
                    res = response_format(FRAMEWORK, value, {})

                elif isinstance(value, list):
                    # params parse fail
                    res = response_format(PARAMS_INVALID, key + value[0], {})

                else:
                    # other situation
                    res = response_format(FRAMEWORK, str(value), {})
                # return custom data
                return Response(res, status=response.status_code, exception=True)

    return response
