from datetime import datetime
from rest_framework.generics import GenericAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializer import RegisterSerializer, LoginSerializer
from utils import response


# Create your views here.
class RegisterView(GenericAPIView):
    """
        注册视图
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        # get request json: request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.success_response('Login success')


class PhoneLoginView(JSONWebTokenAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # json is {'phone': '', 'code': 'xxxx'} or {'phone': '', 'password': ''}
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.object.get('token')
            resp = response.success_response('Log in success', {'token': token})
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                resp.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
            return resp

        return response.fail_response(response.PARAMS_INVALID, 'Unable to log in with provided credentials')
