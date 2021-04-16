from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (Menu, Article, PlugIn, LimitLinkPlugIn)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'isroot', 'isvisible', 'order')
    list_filter = ['isroot', 'isvisible', 'parent_menu']
    list_per_page = 18

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'level', 'isvisible', 'iswrite')
    list_filter = ['isvisible', 'iswrite', 'menu']
    list_per_page = 18

class PlugInAdmin(admin.ModelAdmin):
    list_display = ('url', 'isvalid', 'create_time')
    list_filter = ['isvalid']
    list_per_page = 18

class LimitLinkPlugInAdmin(admin.ModelAdmin):
    list_display = ('access_code', 'times', 'continue_times', 'islegal')
    list_filter = ['user', 'plugin']
    list_per_page = 18

admin.site.register(Menu, MenuAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(PlugIn, PlugInAdmin)
admin.site.register(LimitLinkPlugIn, LimitLinkPlugInAdmin)

admin.site.site_title = _("四象生八卦") # 登录界面的LOGO名
admin.site.site_header = _("四象生八卦") # 后台的LOGO名