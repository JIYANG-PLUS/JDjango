from django.contrib import admin
from .models import Board,Remark,Article,Notice,Suggestion,PlugInSamples,Change,SuggestVote

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['creator']
    list_per_page = 18
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'level', 'modify_time', 'isvisible', 'votes')
    list_filter = ['board']
    list_per_page = 18
class RemarkAdmin(admin.ModelAdmin):
    list_display = ('content', 'votes', 'isroot', 'isvisible', 'create_time')
    list_filter = []
    list_per_page = 18
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'create_time')
    list_filter = []
    list_per_page = 18
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'create_time')
    list_filter = ['isvalid']
    list_per_page = 18
class PlugInSamplesAdmin(admin.ModelAdmin):
    list_display = ('pluginId', 'create_time')
    list_filter = ['pluginId']
    list_per_page = 18
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('create_time',)
    list_filter = []
    list_per_page = 18
class SuggestVoteAdmin(admin.ModelAdmin):
    # list_display = ('',)
    list_filter = ['isvote', 'voter']
    list_per_page = 18

admin.site.register(Board, BoardAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Remark, RemarkAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(PlugInSamples, PlugInSamplesAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(SuggestVote,SuggestVoteAdmin)
