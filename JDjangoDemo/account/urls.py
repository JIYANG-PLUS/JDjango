from django.urls import path, include
from .views import (
    PasswordReset, LogIn, Registry
    , LogOut, ValidCode, RegistryInfo
    , PasswordResetEmailValid, ClickEmailLink
    , PasswordResetSuccess, LogOutBBS, UserInfoView
    , OnlyCodeSendEmail, GenerateOnlyCode
    )

app_name = 'account'

urlpatterns = [
    path('passwordreset/', include([
        path('', PasswordReset.as_view(), name='passwordreset'),
        path('success/', PasswordResetSuccess.as_view(), name='passwordresetsuccess'),
    ])),
    path('json/', include([
        path('code/<str:username>/<str:email>/', ValidCode.as_view()),
        path('registry/<str:username>/<str:email>/<str:pwd>/<str:code>/', RegistryInfo.as_view()),
        path('passwordreset/<str:email>/', PasswordResetEmailValid.as_view()),
        path('onlycodesendemail/', OnlyCodeSendEmail.as_view()),
        path('generateonlycode/<str:code>/', GenerateOnlyCode.as_view()),
    ])),
    path('emailreset/<int:pk>/<slug:slug>/', ClickEmailLink.as_view(), name='emailreset'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut, name='logout'),
    path('logoutBBS/', LogOutBBS, name='logoutBBS'),
    path('registry/', Registry.as_view(), name='registry'),
    path('userinfo/<int:pk>/', include([
        path('', UserInfoView.as_view(), name='userinfo'),
    ])),
]
