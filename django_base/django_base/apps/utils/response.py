from rest_framework.response import Response


# custom response for APIView and GenericAPIView
def my_response(code, msg, data):
    return Response({'code': code, 'success': True if code == 0 else False, 'message': msg, 'data': data})
