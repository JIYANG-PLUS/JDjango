from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone
from .manage import RegistryLogManage,PasswordResetLogManage,OnlyCodeLogManage


# 扩展用户信息
class UserInfo(models.Model):
    token = models.CharField(_("用户唯一标识码"), max_length=32, unique=True)
    # authorization = models.CharField(_("授权码"), max_length=8, default='0')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='other_info', verbose_name=_('所属用户'))
    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = '账户扩展信息'
        verbose_name_plural = '账户扩展信息'

# 独立的一张表（用于临时记录注册信息）
class RegistryLog(models.Model):
    # username = models.CharField(_('用户名'), max_length=6)
    email = models.EmailField(_('邮箱'), unique=True)
    # password = models.CharField(_('密码'), max_length=15)
    code = models.CharField(_("验证码"), max_length=8)
    operate_time = models.DateTimeField(_("初次操作时间"), auto_now_add=True)
    code_time = models.DateTimeField(_("验证码有效期"), auto_now=True)
    objects = models.Manager()
    logManage = RegistryLogManage()
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = '注册临时表'
        verbose_name_plural = '注册临时表'

# 找回密码临时表
class PasswordResetLog(models.Model):
    email = models.EmailField(_('邮箱'), unique=True)
    slug = models.CharField(_("Slug"), max_length=128)
    operate_time = models.DateTimeField(_("初次操作时间"), auto_now_add=True)
    code_time = models.DateTimeField(_("Slug有效期"), auto_now=True)
    objects = models.Manager()
    logManage = PasswordResetLogManage()
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = '重置密码临时表'
        verbose_name_plural = '重置密码临时表'

# 唯一码生成临时表
class OnlyCodeLog(models.Model):
    email = models.EmailField(_('邮箱'), unique=True)
    code = models.CharField(_("验证码"), max_length=8)
    operate_time = models.DateTimeField(_("初次操作时间"), auto_now_add=True)
    code_time = models.DateTimeField(_("验证码有效期"), auto_now=True)
    objects = models.Manager()
    logManage = OnlyCodeLogManage()
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = '唯一码临时表'
        verbose_name_plural = '唯一码临时表'
