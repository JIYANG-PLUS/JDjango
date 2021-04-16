from django.urls import path, include

from .view_plugin import (
    NanJinMetro,
)

urlpatterns = [
    path('nanjinmetro/', NanJinMetro.as_view()), # 南京地铁搜索
]
