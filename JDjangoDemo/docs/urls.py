from django.urls import path, include
from .views import Index

from .views import (
    PkReturnName, PkReturnAll, ContentDetail,
    Menu2Articles, 
    AddMenu, DelMenu, ModifyMenu,
    Vote,JSONPluGinExplain,JSONArticle,
    CheckPlugInActive,CreateAuthorizationCode,
    CheckPlugInActiveContinue,ContinuePlugIn
    )

app_name = 'docs'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('json/', include([
        path('pk2name/<int:pk>/', PkReturnName.as_view(), name='pk2name'),
        path('pk2all/<int:pk>/', PkReturnAll.as_view(), name='pk2all'),
        path('articles/<int:pk>/', Menu2Articles.as_view(), name='articles'),
        path('menu/', include([
            path('add/<str:name>/<str:description>/<int:order>/<int:pk>/<int:isroot>/<int:isvisible>/', AddMenu.as_view(), name='add_menu'),
            path('del/<int:pk>/', DelMenu.as_view(), name='del_menu'),
            path('modify/<str:name>/<str:description>/<int:order>/<int:pk>/<int:isroot>/<int:isvisible>/', ModifyMenu.as_view(), name='modify_menu'),
        ])),
        path('modify/sample/<int:cid>/', JSONPluGinExplain.as_view()),
        path('modify/article/<int:pk>/', JSONArticle.as_view()),
        path('checkpluginactive/<str:p32>/', CheckPlugInActive.as_view()), # 检测接口是否被激活
        path('checkpluginactivecontinue/<str:p32>/', CheckPlugInActiveContinue.as_view()), # 检测接口是否被激活，是否符合续约条件
        path('authorizationcode/<str:p32>/', CreateAuthorizationCode.as_view()), # 给予授权码
        path('continueplugin/<str:p32>/', ContinuePlugIn.as_view()), # 续约
    ])),
    path('content/', include([
        path('<int:pk>/<int:id>/', ContentDetail.as_view(), name='content_index'), # 接收插件pk，和代码样例id
        path('votes/<int:pk>/', Vote.as_view(), name='vote'), # 暂未实现
    ])),
]