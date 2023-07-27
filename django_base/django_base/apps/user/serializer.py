import time
from django.db import DatabaseError
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.compat import PasswordField
from rest_framework_jwt.settings import api_settings

from utils import response
from .models import User


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class RegisterSerializer(serializers.Serializer):
    phone = serializers.RegexField(r'^1[3-9]\d{9}$', required=True, error_messages={'invalid': '手机号格式异常'})
    password = serializers.CharField(required=True)

    def validate_phone(self, value):
        # 验证手机号重复
        count = User.objects.filter(phone=value).count()
        if count != 0:
            raise serializers.ValidationError({'code': response.DUPLICATE, 'message': '手机号已注册', 'data': ''})

        return value

    def create(self, validated_data):
        # 保存数据

        # 拼接username
        username = "用户" + str(time.time())
        try:
            user = User.objects.create_user(username=username, **validated_data)
        except DatabaseError as e:
            print(e)
            return serializers.ValidationError({'code': '510', 'message': '注册失败', 'data': ''})
        return user


class LoginSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(LoginSerializer, self).__init__(*args, **kwargs)

        self.fields['phone'] = serializers.RegexField(r'^1[3-9]\d{9}$', required=True, error_messages={'invalid': 'Phone format error'})
        self.fields['password'] = PasswordField(write_only=True, required=False)
        self.fields['code'] = serializers.RegexField(r'\d{4}$', required=False, error_messages={'invalid': 'Code format error'})

    def validate(self, attrs):
        credentials = {
            'phone': attrs.get('phone')
        }

        if attrs.get('password'):
            credentials['password'] = attrs.get('password')
        elif attrs.get('code'):
            credentials['code'] = attrs.get('code')
        else:
            msg = _('Must include "password" or "code".')
            raise serializers.ValidationError(msg)

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "password" or "code".')
            raise serializers.ValidationError(msg)
