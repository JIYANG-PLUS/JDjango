from django.urls import path, include
from .views import (
    Index,JSONotice,ClickVotes,JSONoticeDetial,
    JSONRecent,ArticleDetial,PlugInSampleDetial,
    BoardDetial,SuggestSuccess,SuggestVotes,
    BoardToArtricles,JSONBoardDetial
    )

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('suggestsuccess/<str:info>/', SuggestSuccess.as_view(), name='suggestsuccess'), # 建议操作成功界面
    # 首页相关的JSON获取
    path('json/', include([
        path('notice/<str:mode>/', JSONotice.as_view()), # 紧急、重要、一般  三类数据返回
        path('notice/detial/<int:pk>/', JSONoticeDetial.as_view()), # 通知详情
        path('recent/<str:mode>/', JSONRecent.as_view()), # 最近更新  时间范围选择
        path('votes/<int:pk>/', ClickVotes.as_view()), # 文章 投票
        path('svotes/<int:spk>/', SuggestVotes.as_view()), # 建议 投票
    ])),
    path('articledetial/<int:pk>/', ArticleDetial.as_view(), name='articledetial'), # 文章详情页
    path('pluginsampledetial/<int:id>/<int:sid>/', PlugInSampleDetial.as_view(), name='pluginsampledetial'), # 插件使用范例详情页
    path('boardetial/', BoardDetial.as_view(), name='boardetial'), # 板块列表页
    path('boardetial/json/<int:pk>/', JSONBoardDetial.as_view()), # 板块列表页
    path('boartoarticles/<int:pk>/', BoardToArtricles.as_view(), name='boartoarticles'), # 版块点击后弹出的文章列表页面
]
