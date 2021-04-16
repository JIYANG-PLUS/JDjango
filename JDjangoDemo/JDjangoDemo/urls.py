from django.contrib import admin
from django.urls import path, include

from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('docs/', include('docs.urls')),
    path('plugin/', include('docs.urls_plugin')),
    path('BBS/', include('blog.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
]
