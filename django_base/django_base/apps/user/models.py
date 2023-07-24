from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """user model"""
    STATUS = (
        (0, '正常'),
        (1, '注销')
    )
    SEX = (
        (0, '男'),
        (1, '女'),
    )

    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=200, verbose_name='密码')
    nick_name = models.CharField(max_length=50, null=True, verbose_name='昵称')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'

    def __str__(self):
        return self.username
