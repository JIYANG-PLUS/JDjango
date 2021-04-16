from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    get_list_or_404,
)
from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (Menu, Article, PlugIn, LimitLinkPlugIn)
from collections import deque
import itertools as iters
from django.core.paginator import Paginator
import json
from datas_tools.datas import Code
from django.db.models import F,Q
coder = Code()
LEN_CODE = 8 # 8位授权码

class Index(View):
    TEMPLATE = 'docs/documentation.html'
    PAGES_NUM = 6 # 每页显示的条数
    def get(self, request):
        root_menus = zip(
            Menu.menuManage.roots, 
            Menu.menuManage.roots, iters.repeat(1)
            )
        all_menus = []
        queue = deque([])
        for _ in root_menus:
            all_menus.append(_)
            queue.extend(zip(
                Menu.menuManage.get_children_nodes(_[0]), 
                iters.repeat(_[0]), iters.repeat(_[2]+1)
                ))
            while 0 != len(queue):
                left = queue.popleft()
                all_menus.append(left)
                queue.extendleft(zip(
                    Menu.menuManage.get_children_nodes(left[0]), 
                    iters.repeat(left[0]), iters.repeat(left[2]+1)
                    ))
        # 分页处理
        articles = Article.objects.all().order_by('-create_time') # 分页前必排序
        paginator = Paginator(articles, self.PAGES_NUM)
        page = request.GET.get('page')
        try:
            datas = paginator.page(page)
        except:
            datas = paginator.page(1)
        return render(request, self.TEMPLATE, {
            'all_menus':all_menus,
            'articles': datas,
            })
    
    def post(self, request):
        if 'plugin_menu_pk' in request.POST:
            plugin_name = request.POST.get('plugin_name', '').strip()
            plugin_menu_pk = request.POST.get('plugin_menu_pk', '').strip()
            plugin_label = request.POST.get('plugin_label', '').strip()
            plugin_abstract = request.POST.get('plugin_abstract', '').strip()
            plugin_version = request.POST.get('plugin_version', '').strip()
            plugin_content = request.POST.get('plugin_content', '').strip()
            plugin_isvisible = request.POST.get('plugin_isvisible', '').strip()
            Article.objects.create(
                title = plugin_name,
                content = plugin_content,
                abstract = plugin_abstract,
                label = plugin_label,
                version = plugin_version,
                isvisible = True if 'on'==plugin_isvisible else False,
                menu = get_object_or_404(Menu, pk=plugin_menu_pk),
                author = request.user
            )
            return redirect('/')
        else:
            return HttpResponse("非法操作，<a href='/'>点此返回</a>");

# 点击菜单，返回菜单下对应的文章信息
class Menu2Articles(View):
    def get(self, request, pk):
        f_menu = get_object_or_404(Menu, pk=pk)
        articles = Article.objects.filter(menu=f_menu).order_by('-create_time')
        list_articles = [
            { 'id': _.id,
            'pk': _.pk,
            'title': _.title,
            'label': _.label,
            'level': _.level,
            'modify_time': f'{_.modify_time:%Y-%m-%d %H:%M:%S}', 
            'abstract': _.abstract} for _ in articles]
        return JsonResponse({
            'articles': list_articles,
            'menu_name': f_menu.name,
        })

# 需权限才能够开启
# 接收pk返回Menu的name
class PkReturnName(LoginRequiredMixin, View):
    def get(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        return JsonResponse({'name': obj.name[:5]})

# 接收pk返回Menu的所有信息
class PkReturnAll(LoginRequiredMixin, View):
    def get(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        return JsonResponse({
            'name': obj.name[:5],
            'full_name': obj.name,
            'description': obj.description,
            'isroot': obj.isroot,
            'isvisible': obj.isvisible,
            'order': obj.order,
        })

# 新增Menu
class AddMenu(LoginRequiredMixin, View):
    def get(self, request, **args):
        name = args['name']
        description = args['description']
        order = args['order']
        pk = args['pk']
        isroot = args['isroot']
        isvisible = args['isvisible']
        try:
            rootMenu = None if 0 == pk else Menu.objects.get(pk=pk)
            menu = Menu.menuManage.new(
                name,description,
                isroot = isroot,
                order = order,
                isvisible = isvisible,
                parent_menu = rootMenu
            )
        except:
            return JsonResponse({'msg':'fail'})
        else:
            return JsonResponse({'msg':'success'})

# 删除Menu
class DelMenu(LoginRequiredMixin, View):
    def get(self, request, **args):
        pk = args['pk']
        try:
            Menu.objects.get(pk=pk).delete()
        except:
            return JsonResponse({'msg':'fail'})
        else:
            return JsonResponse({'msg':'success'})
            
# 修改Menu
class ModifyMenu(LoginRequiredMixin, View):
    def get(self, request, **args):
        name = args['name']
        description = args['description']
        order = args['order']
        pk = args['pk']
        isroot = args['isroot']
        isvisible = args['isvisible']
        try:
            menu = Menu.objects.get(pk=pk)
        except:
            return JsonResponse({'msg':'fail'})
        else:
            menu.name = name
            menu.description = description
            menu.order = order
            menu.isroot = isroot
            menu.isvisible = isvisible
            menu.save()
            return JsonResponse({'msg':'success'})
# 权限结束

# 接口文章详情页
class ContentDetail(View):
    TEMPLATE = 'docs/content.html'
    def get(self, request, pk, id):
        article = get_object_or_404(Article, pk=pk)
        # 查找样例id（为了关联代码样例）
        sampleId = None
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT t.id FROM blog_pluginsamples t WHERE t.pluginId={article.id} """)
            for row in cursor.fetchall():
                sampleId = (row[0])
        plugins = PlugIn.objects.filter(article=article)
        return render(request, self.TEMPLATE, {
            'article': article,
            'sampleId': sampleId,
            'isinsert': True if len(plugins) > 0 else False,
            })
    def post(self, request, pk, id):
        #原生SQL查询
        from django.db import connection
        from django.utils import timezone
        flag = 0
        now_time = timezone.now()
        if 'content' in request.POST: # 新增代码样例
            content = request.POST.get('content', '').strip()
            with connection.cursor() as cursor:
                try:
                    sql = f"""INSERT INTO blog_pluginsamples('content', 'pluginId', 'sampler_id', 'create_time', 'modify_time') VALUES('{content}', '{id}', '{request.user.id}', '{now_time}', '{now_time}')"""
                    cursor.execute(sql)
                except:
                    flag = 1
                else:
                    # 示例撰写完成后在接口中标记
                    Article.objects.filter(id=id).update(iswrite=True) # 用id保持前后一致性
            if 0 == flag:
                return HttpResponse(f'''<h1>附带内容添加成功<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
            else:
                return HttpResponse(f'''<h1>附带内容添加失败<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
        elif 'plugin_menu_pk' in request.POST: # 修改接口文章详情页
            plugin_name = request.POST.get('plugin_name', '').strip()
            plugin_menu_pk = request.POST.get('plugin_menu_pk', '').strip()
            plugin_label = request.POST.get('plugin_label', '').strip()
            plugin_abstract = request.POST.get('plugin_abstract', '').strip()
            plugin_version = request.POST.get('plugin_version', '').strip()
            plugin_content = request.POST.get('plugin_content', '').strip()
            plugin_isvisible = request.POST.get('plugin_isvisible', '').strip()
            # 开始更新
            Article.objects.filter(pk=pk).update(
                title = plugin_name,
                content = plugin_content,
                abstract = plugin_abstract,
                label = plugin_label,
                version = plugin_version,
                isvisible = True if 'on'==plugin_isvisible else False,
            )
            return HttpResponse(f'''<h1>接口文章修改成功<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
        elif 'article_pk' in request.POST: # 关联插件新增
            import uuid
            link_use_linke = request.POST.get('link_use_linke', '').strip()
            link_use_valid = request.POST.get('link_use_valid', '').strip()
            article_pk = request.POST.get('article_pk', '').strip()
            article = get_object_or_404(Article, pk=article_pk)
            if len(PlugIn.objects.filter(url=link_use_linke)) <= 0:
                PlugIn.objects.create(
                    url = link_use_linke,
                    only_code = (str(uuid.uuid4()).replace('-', ''))[:32],
                    isvalid = (True if 'on'==link_use_valid else False),
                    generator = request.user,
                    article = article
                )
                return HttpResponse(f'''<h1>关联接口新增成功<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
            else:
                return HttpResponse(f'''<h1>关联接口已录入（或出现重复接口），请勿重复录入（或联系管理员解决）。<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
        else: # 修改代码样例
            modify_content = request.POST.get('content-modify', '').strip()
            article_id = request.POST.get('id', '').strip()
            with connection.cursor() as cursor:
                try:
                    sql = f"""UPDATE blog_pluginsamples SET content='{modify_content}',modify_time='{now_time}',sampler_id='{request.user.id}' WHERE pluginId='{article_id}'"""
                    cursor.execute(sql)
                except:
                    flag = 1
                else:
                    flag = 0
            if 0 == flag: # 用flag的目的是为了方便释放占用的资源
                return HttpResponse(f'''<h1>附带内容修改成功<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')
            else:
                return HttpResponse(f'''<h1>附带内容修改失败<h1><a href='/docs/content/{pk}/{id}/'>点此返回</a>''')

# 获取旧代码样例信息
class JSONPluGinExplain(View):
    def get(self, request, cid):
        from django.db import connection
        content = ''
        with connection.cursor() as cursor:
            try:
                sql = f"""SELECT content FROM blog_pluginsamples WHERE pluginId={cid}"""
                cursor.execute(sql)
                for row in cursor.fetchall():
                    content = row[0]
            except: pass
            else: pass
        return JsonResponse({
            'content': content,
        })

# 获取旧插件文章信息
class JSONArticle(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return JsonResponse({
            'name': article.title,
            'label': article.label,
            'abstract': article.abstract,
            'version': article.version,
            'content': article.content,
            'isvisible': article.isvisible,
        })

# 投票【功能待定】
class Vote(View):
    def get(self, request, pk):
        return JsonResponse({})

# 检测接口是否存在并激活剩余操作
class CheckPlugInActive(LoginRequiredMixin, View):
    def get(self, request, p32):
        plugins = PlugIn.objects.filter(only_code=p32)
        if len(plugins) > 0:
            return JsonResponse({
                'msg':'success',
                'url': plugins[0].url,
                'isvalid': plugins[0].isvalid,
                'title': plugins[0].article.title,
                })
        else:
            return JsonResponse({'msg':'failure'})

# 用户申请对应接口的授权码
class CreateAuthorizationCode(LoginRequiredMixin, View):
    def get(self, request, p32):
        plugin = get_object_or_404(PlugIn, only_code=p32)
        code = coder.get_code(LEN_CODE)
        objs = LimitLinkPlugIn.objects.filter(Q(plugin=plugin)&Q(user=request.user)) # 这里需要加条件
        if len(objs) > 0:
            return JsonResponse({'msg':'failure'}) 
        try:
            LimitLinkPlugIn.objects.create(
                access_code = code,
                times = 100,
                user = request.user,
                plugin = plugin
            )
        except:
            return JsonResponse({'msg':'failure'})
        else:
            return JsonResponse({'msg':'success'})

# 检测接口是否存在，是否符合续约条件
class CheckPlugInActiveContinue(LoginRequiredMixin, View):
    def get(self, request, p32):
        plugins = PlugIn.objects.filter(only_code=p32)
        if len(plugins) > 0: # 首先验证接口是否存在
            # 验证用户是否已使用过接口，并且当前的剩余次数小于等于10
            try:
                objs = request.user.ulimits.filter(plugin=plugins[0])
            except:
                return JsonResponse({'msg':'failure'})
            else:
                if len(objs)<=0 or objs[0].times > 10 or objs[0].islegal:
                    return JsonResponse({'msg':'failure'})
                else:
                    # 仅检测，不操作
                    return JsonResponse({
                        'msg':'success',
                        'url': plugins[0].url,
                        'isvalid': plugins[0].isvalid,
                        'title': plugins[0].article.title,
                        })
        else:
            return JsonResponse({'msg':'failure'})

# 接口码续约
class ContinuePlugIn(LoginRequiredMixin, View):
    def get(self, request, p32):
        plugins = PlugIn.objects.filter(only_code=p32)
        if len(plugins) > 0: # 首先验证接口是否存在
            # 验证用户是否已使用过接口，并且当前的剩余次数小于等于10
            try:
                objs = request.user.ulimits.filter(plugin=plugins[0])
            except:
                return JsonResponse({'msg':'failure'})
            else:
                if len(objs)<=0 or objs[0].times > 10 or objs[0].islegal:
                    return JsonResponse({'msg':'failure'})
                else:
                    # 续约
                    objs[0].times = 100
                    objs[0].continue_times = F('continue_times') + 1
                    objs[0].save()
                    return JsonResponse({'msg':'success'})
        else:
            return JsonResponse({'msg':'failure'})
