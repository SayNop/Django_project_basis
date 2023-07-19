from django_redis import get_redis_connection
from django.contrib.auth.backends import ModelBackend


class UsernameMobileAuthBackend(ModelBackend):
    """custom auth backend"""
    def authenticate(self, request, username=None, password=None, code=None, is_backend=None, **kwargs):
        """
        return user object
        """
        # user login auth
        if not is_backend:
            if not username:
                return
            # sms code login
            if code is not None:
                redis_conn = get_redis_connection('verify_code')
                sms_code_server = redis_conn.get('sms_%s' % username)
                if sms_code_server is None:
                    return None
                if code != sms_code_server.decode():
                    return None
                try:
                    user = User.objects.get(username=username)
                except:
                    return None
                # 判断密码
                else:
                    return user
            # password login
            else:
                # find user obj
                try:
                    user = User.objects.get(username=username)
                except:
                    # 如果未查到数据，则返回None，用于后续判断
                    try:
                        user = User.objects.get(phone=username)
                    except:
                        return None
                # check password
                if user.check_password(password):
                    return user

                else:
                    return None

        # admin login auth (mis)
        else:
            try:
                user = User.objects.get(username=username, is_staff=True)
            except:
                return
                # 判断密码
            if user is not None and user.check_password(password):
                return user
