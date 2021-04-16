from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone
from .manage import MenuManage, ArticleManage

LEVELS = [
    ('a', 'A级'),
    ('b', 'B级'),
    ('c', 'C级'),
    ('d', 'D级'),
    ('e', 'E级'),
    ('f', 'F级'),
    ('g', 'G级'),
    ('h', 'H级'),
    ('i', 'I级'),
] # 九级区分，A级最低，I级最高

# 菜单在这里可以理解为板块
class Menu(models.Model):
    name = models.CharField(_("节点名"), max_length=30)
    description = models.TextField(_("节点描述"))
    isroot = models.BooleanField(_("是否根节点"), default=False)
    isvisible = models.BooleanField(_("是否可见"), default=True)
    order = models.PositiveIntegerField(_("节点顺序"), default=0)
    parent_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_menu', verbose_name=_('上级节点'))
    url_path = models.CharField(_("页面绑定"), max_length=60, default='', blank=True)
    add_time = models.DateTimeField(_("添加时间"), auto_now_add=True)
    # 管理器
    objects = models.Manager() # 默认
    menuManage = MenuManage() # 自定义全部

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'

class Article(models.Model):
    title = models.CharField(_("标题"), max_length=100)
    content = models.TextField(_("内容"))
    abstract = models.CharField(_("摘要"), max_length=100)
    label = models.CharField(_("标签"), max_length=100)
    level = models.CharField(_("文章评级"), max_length=1, choices=LEVELS, default='a')
    version = models.CharField(_("版本号"), default='1.0.0', max_length=30)
    create_time = models.DateTimeField(_("创建时间"), auto_now_add=True)
    modify_time = models.DateTimeField(_("修改时间"), auto_now=True)
    isvisible = models.BooleanField(_("是否可见"), default=True)
    iswrite = models.BooleanField(_("是否已撰写示例"), default=False)
    url_path = models.CharField(_("页面绑定"), max_length=60, default='', blank=True)
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='marticles', verbose_name=_('所属菜单'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warticles', verbose_name=_('作者'))
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aarticles', verbose_name=_('审核人'), null=True, blank=True)
    # 管理器
    objects = models.Manager() # 默认
    articleManage = ArticleManage() # 自定义
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '接口文章'
        verbose_name_plural = '接口文章'

# Article的互动扩展【暂时搁置的功能】
class ArticleA(models.Model):
    use_time = models.PositiveIntegerField(_("调用次数"), default=0)
    votes = models.PositiveIntegerField(_("支持数"), default=0)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='articleA', verbose_name=_('接口'))
    def __str__(self):
        return 'articleA'
    class Meta:
        verbose_name = '接口互动'
        verbose_name_plural = '接口互动'

# Article的评论【暂时搁置的功能】
class Remark(models.Model):
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

# 接口类
class PlugIn(models.Model):
    url = models.URLField(_("接口"), unique=True)
    only_code = models.CharField(_("接口唯一标识"), max_length=32, unique=True)
    isvalid = models.BooleanField(_("可用"), default=True)
    create_time = models.DateTimeField(_("创建时间"), auto_now_add=True)
    generator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls', verbose_name=_('创作者'))
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='aurls', verbose_name=_('关联文章'))
    def __str__(self):
        return self.url
    class Meta:
        verbose_name = '接口注册'
        verbose_name_plural = '接口注册'

# 接口授权码
class LimitLinkPlugIn(models.Model):
    access_code = models.CharField(_("授权码"), max_length=8)
    times = models.PositiveIntegerField(_("剩余调用次数"), default=100)
    continue_times = models.PositiveIntegerField(_("续约次数"), default=0)
    islegal = models.BooleanField(_("禁用"), default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulimits', verbose_name=_('使用者'))
    plugin = models.ForeignKey(PlugIn, on_delete=models.CASCADE, related_name='plimits', verbose_name=_('接口'))
    def __str__(self):
        return self.access_code
    class Meta:
        verbose_name = '授权码'
        verbose_name_plural = '授权码'
