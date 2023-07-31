import time
from django.db import DatabaseError
from django.contrib.auth import authenticate
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
    phone = serializers.RegexField(r'^1[3-9]\d{9}$', required=True, error_messages={'invalid': 'Phone format error'})
    password = serializers.CharField(required=True)

    def validate_phone(self, value):
        # check user exist
        count = User.objects.filter(phone=value).count()
        if count != 0:
            raise serializers.ValidationError(response.fail_response(response.DUPLICATE, 'Already Register'))

        return value

    def create(self, validated_data):
        # save user object
        # username
        username = "User" + str(time.time())
        try:
            user = User.objects.create_user(username=username, **validated_data)
        except DatabaseError as e:
            print(e)
            return serializers.ValidationError(response.fail_response(msg='Register fail'))
        return user


class LoginSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        """
        sms login or password login
        {'phone': '', 'code': xxxx} or {'phone': '', 'password': xxxx}
        """
        super(LoginSerializer, self).__init__(*args, **kwargs)

        self.fields['phone'] = serializers.RegexField(r'^1[3-9]\d{9}$', required=True,
                                                      error_messages={'invalid': 'Phone format error'})
        self.fields['password'] = PasswordField(write_only=True, required=False)
        self.fields['code'] = serializers.RegexField(r'\d{4}$', required=False,
                                                     error_messages={'invalid': 'Code format error'})

    def validate(self, attrs):
        credentials = {
            'phone': attrs.get('phone')
        }

        if attrs.get('password'):
            credentials['password'] = attrs.get('password')
        elif attrs.get('code'):
            credentials['code'] = attrs.get('code')
        else:
            raise serializers.ValidationError(response.fail_response(response.PARAMS_INVALID,
                                                                     'Must include "password" or "code"'))

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(response.fail_response(response.PERMISSION_DENIED,
                                                                             'User account is disabled'))
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                raise serializers.ValidationError(response.fail_response(response.PARAMS_INVALID,
                                                                         'Unable to log in with provided credentials.'))
        else:
            raise serializers.ValidationError(response.fail_response(response.PARAMS_INVALID,
                                                                     'Must include "password" or "code"'))
