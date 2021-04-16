from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# 注册临时表
class RegistryLogManage(models.Manager):
    def new(self,email,code):
        return self.create(
            email=email,
            code=code
            )

    # 验证有效期，验证码的有效期为15分钟
    def validity(self, email):
        pre_user = self.isValidity(email)
        if pre_user[0]:
            if (timezone.now() - pre_user[1].code_time).total_seconds()/60 <= 15: # 15分钟有效期
                return True
            else:
                return False
        else:
            return False

    # 是否是预认证用户
    def isValidity(self, email):
        try:
            pre_user = self.get(email=email)
        except:
            return False, None
        else:
            return True, pre_user

# 重置密码临时表
class PasswordResetLogManage(models.Manager):
    def new(self,email,slug):
        return self.create(
            email=email,
            slug=slug
            )

    # 验证有效期，验证码的有效期为15分钟
    def validity(self, email):
        pre_user = self.isValidity(email)
        if pre_user[0]:
            if (timezone.now() - pre_user[1].code_time).total_seconds()/60 <= 15: # 15分钟有效期
                return True
            else:
                return False
        else:
            return False

    # 是否是预认证用户
    def isValidity(self, email):
        try:
            pre_user = self.get(email=email)
        except:
            return False, None
        else:
            return True, pre_user

# 唯一码临时表
class OnlyCodeLogManage(models.Manager):
    def new(self,email,code):
        return self.create(
            email=email,
            code=code
            )

    # 验证有效期，验证码的有效期为15分钟
    def validity(self, email):
        pre_user = self.isValidity(email)
        if pre_user[0]:
            if (timezone.now() - pre_user[1].code_time).total_seconds()/60 <= 15: # 15分钟有效期
                return True
            else:
                return False
        else:
            return False

    # 是否是预认证用户
    def isValidity(self, email):
        try:
            pre_user = self.get(email=email)
        except:
            return False, None
        else:
            return True, pre_user
