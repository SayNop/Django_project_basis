from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    """
    LoginSerializer
    """
    phone = serializers.RegexField(r'^1[3-9]\d{9}$', required=True, error_messages={'invalid': '手机号格式异常'})
    password = serializers.CharField(required=True)
