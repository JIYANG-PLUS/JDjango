from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

class MenuManage(models.Manager):
    def new(self,name,description,isroot=False,isvisible=True,order=0,parent_menu=None):
        if None == parent_menu:
            return self.create(
                name=name,
                description=description,
                isroot=isroot,order=order,
                isvisible=isvisible
                )
        else:
            return self.create(
                name=name,
                description=description,
                isroot=isroot,order=order,
                isvisible = isvisible,
                parent_menu=parent_menu
                )
    
    def get_queryset(self):
        return super().get_queryset().all() # 数据源为全部

    @property
    def roots(self):
        return self.filter(Q(isroot=True)&Q(isvisible=True)).order_by('order')

    # 获取某节点下的所有可见孩子节点【非子孙节点】
    def get_children_nodes(self, root):
        return self.filter(Q(parent_menu=root)&Q(isvisible=True))

    # 判断两节点是否全等
    def equals(self, item1, item2):
        if item1.pk == item2.pk:
            return True
        else:
            return False

class ArticleManage(models.Manager):
    def new(self):
        pass
    
    def get_queryset(self):
        return super().get_queryset().all()