from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone

from .manage import ArticleManage,RemarkManage,SuggestVoteManage

# 文章等级
LEVELS = [
    ('a', _('A级')),
    ('b', _('B级')),
    ('c', _('C级')),
    ('d', _('D级')),
    ('e', _('E级')),
    ('f', _('F级')),
    ('g', _('G级')),
    ('h', _('H级')),
    ('i', _('I级')),
] # 九级区分，A级最低，I级最高

# 公告紧急状态
NOTICE_LEVEL = [
    ('A', _('一般')),
    ('B', _('重要')),
    ('C', _('紧急')),
]

class Board(models.Model):
    name = models.CharField(_("板块名"), max_length=30)
    description = models.TextField(_("板块描述"))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards', verbose_name=_('创建人'))
    create_time = models.DateTimeField(_("添加时间"), auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '板块'
        verbose_name_plural = '板块'

class Article(models.Model):
    title = models.CharField(_("标题"), max_length=100)
    content = models.TextField(_("内容"))
    abstract = models.CharField(_("摘要"), max_length=100)
    label = models.CharField(_("标签"), max_length=100)
    level = models.CharField(_("文章评级"), max_length=1, choices=LEVELS, default='a')
    create_time = models.DateTimeField(_("创建时间"), auto_now_add=True)
    modify_time = models.DateTimeField(_("修改时间"), auto_now=True)
    isvisible = models.BooleanField(_("是否可见"), default=True)
    isgood = models.BooleanField(_("是否精选"), default=False)
    url_path = models.CharField(_("页面绑定"), max_length=60, default='', blank=True)
    votes = models.PositiveIntegerField(_("支持率"), default=0)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='b_articles', verbose_name=_('所属板块'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='r_articles', verbose_name=_('作者'))
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='a_articles', verbose_name=_('审核人'), null=True, blank=True)
    # 管理器
    objects = models.Manager() # 默认
    articleManage = ArticleManage() # 自定义全部
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

class Remark(models.Model):
    content = models.TextField(_("评论内容"))
    votes = models.PositiveIntegerField(_("支持率"), default=0)
    isroot = models.BooleanField(_("是否根评论"), default=True) # 默认根评论
    isvisible = models.BooleanField(_("是否可见"), default=True)
    create_time = models.DateTimeField(_("评论时间"), auto_now_add=True)
    remarker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rremarks', verbose_name=_('评论人'))
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='remarks', verbose_name=_('文章'))
    parent_remark = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_remark', verbose_name=_('上级评论'))
    # 管理器
    objects = models.Manager() # 默认
    remarkManage = RemarkManage() # 自定义全部
    def __str__(self):
        return 'remark'
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

class Notice(models.Model):
    title = models.CharField(_("公告标题"), max_length=100)
    content = models.TextField(_("公告内容"))
    accept = models.PositiveIntegerField(_("收到"), default=0)
    level = models.CharField(_("紧急情况"), max_length=1, choices=NOTICE_LEVEL, default='A')
    create_time = models.DateTimeField(_("公告时间"), auto_now_add=True)
    noticer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices', verbose_name=_('发布人'))
    def __str__(self):
        return 'notice'
    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

class Suggestion(models.Model):
    content = models.TextField(_("建议内容"))
    create_time = models.DateTimeField(_("发布时间"), auto_now_add=True)
    isvalid = models.BooleanField(_("参与投票"), default=False)
    votes = models.PositiveIntegerField(_("投票数"), default=0)
    suggester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggests', verbose_name=_('建议人'))
    def __str__(self):
        return self.content[:8]
    class Meta:
        verbose_name = '建议'
        verbose_name_plural = '建议'

class SuggestVote(models.Model):
    isvote = models.BooleanField(_("已投票"), default=False)
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes', verbose_name=_('投票人'))
    suggest = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='svotes', verbose_name=_('建议'))
    # 管理器
    objects = models.Manager() # 默认
    voteManage = SuggestVoteManage() # 自定义全部
    def __str__(self):
        return self.voter.username+'-'+self.suggest.content
    class Meta:
        verbose_name = '建议投票情况'
        verbose_name_plural = '建议投票情况'

class PlugInSamples(models.Model):
    content = models.TextField(_("示例内容"))
    create_time = models.DateTimeField(_("发布时间"), auto_now_add=True)
    modify_time = models.DateTimeField(_("修改时间"), auto_now=True)
    pluginId = models.PositiveIntegerField(_("父id"))
    sampler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='samples', verbose_name=_('作者'))
    def __str__(self):
        return 'samples'
    class Meta:
        verbose_name = '范例'
        verbose_name_plural = '范例'

class Change(models.Model):
    content = models.TextField(_("变更内容"))
    create_time = models.DateTimeField(_("变更时间"), auto_now_add=True)
    def __str__(self):
        return 'change'
    class Meta:
        verbose_name = '变更'
        verbose_name_plural = '变更'
