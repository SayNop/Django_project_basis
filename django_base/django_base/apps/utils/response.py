from rest_framework.response import Response

SUCCESS = 0

# framework code
FRAMEWORK = 1

# auth code
TOKEN_INVALID = 1000
TOKEN_EXPIRY = 1001
TOKEN_CONFLICT = 1002
PERMISSION_DENIED = 1003

# request
PARAMS_INVALID = 2000
NOT_FOUND = 2001
DUPLICATE = 2002


def response_format(code, msg, data):
    return {'code': code, 'success': True if code == 0 else False, 'message': msg, 'data': data}


# custom response for APIView and GenericAPIView
def success_response(msg='OK', data={}):
    return Response(response_format(SUCCESS, msg, data))


def fail_response(code=FRAMEWORK, msg='Request fail', data={}):
    return Response(response_format(code, msg, data))
