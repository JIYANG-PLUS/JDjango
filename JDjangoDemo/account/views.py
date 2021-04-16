from django.shortcuts import render
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.views.generic import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import RegistryLog, PasswordResetLog, UserInfo, OnlyCodeLog
from smtplib import SMTPException
from datas_tools.datas import Code
from django.urls import reverse

coder = Code()
LEN_CODE = 8 # 邮箱验证码的长度
MY_EMAIL = 'l1129697250@163.com' # 发送人邮箱
URL_HEAD = 'http://127.0.0.1:8000' # 头部链接

# 身份验证的类写法
# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'

# 登录
class LogIn(View):
    TEMPLATE = 'account/login.html'
    TEMPLATE_SUCCESS = 'account/login_failure.html' # 这里是测试
    def get(self, request):
        return render(request, self.TEMPLATE, {})

    def post(self, request):
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request, username=username, password=password) # 验证用户
        if user is not None:
            login(request, user) # 验证成功，登录
            return redirect('/docs/')
        else:
            return render(request, self.TEMPLATE_SUCCESS, {}) # 这里需要修改

# 验证邮箱是否有效
def check_email(email):
    if not (email.endswith('@qq.com') or email.endswith('@foxmail.com') or email.endswith('@163.com')):
        return False
    return True

# 验证该邮箱是否已经注册
def check_email_alive(email):
    temp_user = User.objects.filter(email=email)
    if 0 == len(temp_user):
        return False # 未注册
    return True # 已注册

# 验证用户名是否已注册
def check_username_alive(username):
    temp_user = User.objects.filter(username=username)
    if 0 == len(temp_user):
        return False # 未注册
    return True # 已注册

# 获取验证码
class ValidCode(View):
    def get(self, request, username, email):
        if not check_email(email):
            return JsonResponse({'msg':'fail','code':1}) # 1表示邮箱不符合约定
        if check_username_alive(username):
            return JsonResponse({'msg':'fail','code':5}) # 5表示用户名已被注册
        if check_email_alive(email):
            return JsonResponse({'msg':'fail','code':4}) # 4表示邮箱已被注册
        info = {}
        code = coder.get_code(LEN_CODE)
        try:
            status = send_mail(
                    '注册-四象生八卦',
                    f'注册码【{code}】（大小写敏感），请在15分钟之内完成验证，15分钟后验证码将失效。(本消息为机器发送，勿回复)',
                    MY_EMAIL,
                    [email],
                    fail_silently=False,
                )
        except SMTPException:
            info['msg'] = 'fail'
            info['code'] = 2 # 2网络错误或邮箱不存在
        else:
            if 1 == status: # 成功发送一条验证码
                temp = RegistryLog.objects.filter(email=email)
                if len(temp) > 0: # 已存在，直接更新验证码
                    temp[0].code = code
                    temp[0].save()
                else: # 从未注册过，就新增一条记录
                    RegistryLog.logManage.new(email, code)
                info['msg'] = 'success'
            else:
                info['msg'] = 'fail'
                info['code'] = 3 # 3发送失败
        return JsonResponse(info)

# 发送唯一码的验证邮箱
class OnlyCodeSendEmail(LoginRequiredMixin, View):
    def get(self, request):
        info = {}
        code = coder.get_code(LEN_CODE)
        try:
            status = send_mail(
                    '验证码-四象生八卦',
                    f'验证码【{code}】（大小写敏感），请在15分钟之内完成操作，15分钟后验证码将失效。(本消息为机器发送，勿回复)',
                    MY_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
        except SMTPException:
            info['msg'] = 'fail'
        else:
            # 记录发送信息
            temp = OnlyCodeLog.objects.filter(email=request.user.email)
            if len(temp) > 0:
                temp[0].code = code
                temp[0].save()
            else:
                OnlyCodeLog.logManage.new(request.user.email, code)
            info['msg'] = 'success'
        return JsonResponse(info)

# 生成唯一码
class GenerateOnlyCode(LoginRequiredMixin, View):
    def get(self, request, code):
        # 验证账户是否有效，验证码是否有效
        try:
            log = OnlyCodeLog.objects.get(email=request.user.email)
        except:
            return JsonResponse({'msg':'failure'})
        else:
            # 验证码是否在有效期内
            if OnlyCodeLog.logManage.validity(request.user.email):
                # 验证码是否匹配
                if log.code == code:
                    import uuid
                    token = str(uuid.uuid3(uuid.NAMESPACE_DNS, request.user.email)).replace('-', '')[:32]
                    try:
                        UserInfo.objects.create(token=token, user=request.user)
                    except:
                        return JsonResponse({'msg':'failure'})
                    else:
                        return JsonResponse({'msg':'success'})
                else: return JsonResponse({'msg':'failure'})
            else:
                return JsonResponse({'msg':'failure'})

# 正式注册，并返回注册反馈信息
class RegistryInfo(View):
    def get(self, request, username, email, pwd, code):
        try:
            log = RegistryLog.objects.get(email=email)
        except:
            return JsonResponse({'msg':'failure', 'code':1}) # 1表示获取验证码与实际注册账户不符
        else:
            # 验证码是否在有效期内
            if RegistryLog.logManage.validity(email):
                # 验证码是否匹配
                if log.code == code:
                    try:
                        user = User.objects.create_user(username, email, pwd)
                    except:
                        return JsonResponse({'msg':'failure', 'code':3}) # 3表示用户名重复
                    else:
                        user.save()
                        return JsonResponse({'msg':'success'})
                else: return JsonResponse({'msg':'failure', 'code':2}) # 2表示验证码失效
            else:
                return JsonResponse({'msg':'failure', 'code':2}) # 2表示验证码失效

# 注销，返回到docs主页
@login_required
def LogOut(request):
    logout(request)
    return redirect('/docs/')

# 注销，返回到blog主页
@login_required
def LogOutBBS(request):
    logout(request)
    return redirect('/BBS/')

# 注册页面展示
class Registry(View):
    TEMPLATE = 'account/registry.html'
    def get(self, request):
        return render(request, self.TEMPLATE, {})

# 重置密码
class PasswordReset(View):
    TEMPLATE = 'account/passwordreset.html'
    def get(self, request):
        return render(request, self.TEMPLATE, {})

# 重置密码邮箱验证
class PasswordResetEmailValid(View):
    def get(self, request, email):
        if check_email_alive(email):
            slug = coder.get_code_complex(128) # 生成随机码
            user = User.objects.get(email=email) # 获取用户pk
            url = reverse('account:emailreset', kwargs={'pk': user.pk, 'slug': slug}) # kwargs={'pk': self.pk}
            # 如果用户已重置过，则只需更新slug即可
            temp = PasswordResetLog.objects.filter(email=email)
            if len(temp) > 0: # 已存在，直接更新验证码
                temp[0].slug = slug
                temp[0].save()
            else: # 从未注册过，就新增一条记录
                PasswordResetLog.logManage.new(email, slug)
            # 发送重置密码链接邮箱
            try:
                send_mail(
                        '找回密码-四象生八卦',
                        f'请勿向第三者透露此链接。点击链接 {URL_HEAD}{url} 以重置密码。（此处若点不开，请复制粘贴到浏览器打开）【请在15分钟之内完成密码重置，过时请重新发起申请】(如非本人操作，请忽略此信息)',
                        MY_EMAIL,
                        [email],
                        fail_silently=False,
                    )
            except:
                return JsonResponse({'msg':'failure','code':1}) # 1邮箱未注册
            else:
                return JsonResponse({'msg':'success'})
        else:
            return JsonResponse({'msg':'failure','code':1}) # 1邮箱未注册

# 邮箱链接点击验证
class ClickEmailLink(View):
    TEMPLATE = 'account/emailreset.html'
    ERROR_TEMPLATE = 'account/ill.html'
    def get(self, request, pk, slug):
        # 验证slug是否合法，是否为正常操作
        try:
            user = User.objects.get(pk=pk)
        except:
            return render(request, self.ERROR_TEMPLATE, {})
        else:
            log = PasswordResetLog.objects.get(email=user.email)
            if slug == log.slug and PasswordResetLog.logManage.validity(user.email):
                return render(request, self.TEMPLATE, {'name': user.username})
            else:
                return render(request, self.ERROR_TEMPLATE, {})
    
    def post(self, request, pk, slug):
        pwd = request.POST['password']
        try:
            user = User.objects.get(pk=pk)
        except:
            return render(request, self.ERROR_TEMPLATE, {})
        else:
            log = PasswordResetLog.objects.get(email=user.email)
            if slug == log.slug and PasswordResetLog.logManage.validity(user.email):
                user.set_password(pwd)
                user.save()
                return redirect('account:passwordresetsuccess')
            else:
                return render(request, self.ERROR_TEMPLATE, {})

# 密码重置成功
class PasswordResetSuccess(View):
    TEMPLATE = 'account/reset_success.html'
    def get(self, request):
        return render(request, self.TEMPLATE, {})

# 个人用户界面
class UserInfoView(LoginRequiredMixin, View):
    TEMPLATE = 'account/userinfo.html'
    def get(self, request, pk):
        return render(request, self.TEMPLATE, {})
