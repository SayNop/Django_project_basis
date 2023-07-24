from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_jwt.views import

from .serializer import RegisterSerializer


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
        return Response({'status': 0, 'message': 'OK'})
