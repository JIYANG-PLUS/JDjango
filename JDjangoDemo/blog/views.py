from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import View
from .models import Notice, Article, Change, PlugInSamples, Suggestion, SuggestVote, Board
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import F,Q
from django.contrib.auth.models import User

def noticeToJson(notices):
    objs = []
    for _ in notices:
        objs.append({
            'title': _.title,
            'level': _.level,
            'create_time': f'{_.create_time:%Y-%m-%d %H:%M:%S}',
            'pk': _.pk,
        })
    return objs

def articleToJson(articles):
    objs = []
    for _ in articles:
        objs.append({
            'title': _.title,
            'modify_time': f'{_.modify_time:%Y-%m-%d %H:%M:%S}',
            'pk': _.pk,
        })
    return objs

class Index(View):
    TEMPLATE = 'blog/index.html'
    SEARCH_TEMPLATE = 'blog/article_search.html'
    def get(self, request):
        # 取公告
        notices = Notice.objects.all().order_by('-create_time')[:3]
        # 取【最近更新】文章
        articles = Article.objects.all().order_by('-create_time')[:8]
        # 取精选文章
        goodArticles = Article.articleManage.goodChoiceArticles[:8]
        # 取接口使用范例
        from django.db import connection
        samples = []
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT t1.id,t2.title,t2.id FROM blog_pluginsamples t1 LEFT JOIN docs_article t2 ON t1.pluginId=t2.id""")
            for row in cursor.fetchall():
                samples.append((row[0], row[1], row[2]))
        # 变更通知
        changes = Change.objects.all().order_by('-create_time')
        # 参与投票的建议
        vote_suggests = Suggestion.objects.filter(isvalid=True)
        # 网页响应
        return render(request, self.TEMPLATE, {
            'notices': notices,
            'goodArticles': goodArticles,
            'articles': articles,
            'samples': samples,
            'changes': changes,
            'vote_suggests': vote_suggests,
        })
    
    def post(self, request):
        # 判断是搜索还是提交意见
        if 'suggestion' in request.POST: # 提交建议
            sugg = request.POST.get('suggestion').strip()
            obj = Suggestion.objects.create(
                content = sugg,
                suggester = request.user
            )
            obj.save()
            # 意见提交后建立与用户的投票关系
            u_vs = (SuggestVote(voter=_,suggest=obj) for _ in User.objects.all())
            SuggestVote.objects.bulk_create(u_vs) # 批量插入
            return redirect('blog:suggestsuccess', info='意见提交')
        else: # 搜索框
            # 获取关键词
            search = request.POST.get('search-good').strip()
            # 标签匹配和标题匹配
            articles = Article.objects.filter(Q(abstract__icontains=search)|Q(label__icontains=search)|Q(title__icontains=search))
            return render(request, self.SEARCH_TEMPLATE, {
                'articles':articles,
                'key': search,
                })

# 建议提交成功页
class SuggestSuccess(View):
    TEMPLATE = 'blog/suggest_success.html'
    def get(self, request, info):
        return render(request, self.TEMPLATE, {'info':info})

# 公告
class JSONotice(View):
    # 一般 A、重要 B、紧急 C、ALL D
    def get(self, request, mode):
        notices = None
        if 'A' == mode:
            notices = Notice.objects.filter(level='A').order_by('-create_time')[:3]
        elif 'B' == mode:
            notices = Notice.objects.filter(level='B').order_by('-create_time')[:3]
        elif 'C' == mode:
            notices = Notice.objects.filter(level='C').order_by('-create_time')[:3]
        else:
            notices = Notice.objects.all().order_by('-create_time')[:3]
        return JsonResponse({'notices':noticeToJson(notices)})

# 最近更新
class JSONRecent(View):
    # 近半年 A、近一月 B、近半月 C、近一周 D、ALL E
    def get(self, request, mode):
        articles = None
        if 'A' == mode:
            articles = Article.articleManage.duringHalfYearA.order_by('-create_time')[:8]
        elif 'B' == mode:
            articles = Article.articleManage.duringMonthA.order_by('-create_time')[:8]
        elif 'C' == mode:
            articles = Article.articleManage.duringHalfMonthA.order_by('-create_time')[:8]
        elif 'D' == mode:
            articles = Article.articleManage.duringWeekA.order_by('-create_time')[:8]
        else:
            articles = Article.objects.all().order_by('-create_time')[:8]
        return JsonResponse({'articles':articleToJson(articles)})

# 文章详情页
class ArticleDetial(View):
    TEMPLATE = 'blog/documentation.html'
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return render(request, self.TEMPLATE, {
            'article': article,
        })

# 插件使用范例详情页
class PlugInSampleDetial(View):
    TEMPLATE = 'blog/explain.html'
    def get(self, request, id, sid):
        plugin = None
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT t.id,t.title,t.version FROM docs_article t WHERE t.id={sid} """)
            for row in cursor.fetchall():
                plugin = (row[0], row[1], row[2])
        sample = get_object_or_404(PlugInSamples, id=id)
        return render(request, self.TEMPLATE, {
            'plugin': plugin,
            'sample': sample,
        })

# 板块列表页
class BoardDetial(View):
    TEMPLATE = 'blog/board.html'
    def get(self, request):
        boards = Board.objects.all()
        return render(request, self.TEMPLATE, {
            'boards': boards,
        })
    def post(self, request):
        if 'modify_board_pk' in request.POST: # 修改
            modify_name = request.POST.get('modify_name').strip()
            modify_description = request.POST.get('modify_description').strip()
            modify_board_pk = request.POST.get('modify_board_pk').strip()
            Board.objects.filter(pk=modify_board_pk).update(
                name = modify_name,
                description = modify_description
            )
            return HttpResponse('修改成功，<a href="/BBS/boardetial/">点此返回</a>')
        else: # 新增
            add_name = request.POST.get('add_name').strip()
            add_description = request.POST.get('add_description').strip()
            Board.objects.create(
                name = add_name,
                description = add_description,
                creator = request.user
            )
            return HttpResponse('新增成功，<a href="/BBS/boardetial/">点此返回</a>')

# 修改版块信息JSON返回数据
class JSONBoardDetial(LoginRequiredMixin, View):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        return JsonResponse({
            'name': board.name,
            'description': board.description,
        })

# 版块点击后弹出的文章列表页面
class BoardToArtricles(View):
    TEMPLATE = 'blog/board_articles.html'
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        articles = Article.objects.filter(board__pk=pk)
        return render(request, self.TEMPLATE, {
            'board': board,
            'articles': articles,
        })

# 文章点击投票
class ClickVotes(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.votes = F('votes') + 1
        article.save()
        return JsonResponse({
            'nums': get_object_or_404(Article, pk=pk).votes,
        })

# 意见点击投票
class SuggestVotes(LoginRequiredMixin, View):
    def get(self, request, spk):
        # 检测有没有投票的资格
        s_obj = get_object_or_404(Suggestion, pk=spk)
        obj = get_object_or_404(SuggestVote, voter=request.user, suggest=s_obj)
        if obj.isvote:
            return JsonResponse({'msg':'fail'})
        else:
            # 进行投票
            s_obj.votes = F('votes') + 1
            s_obj.save()
            # obj进行已投票绑定
            obj.isvote = True
            obj.save()
            return JsonResponse({'msg':'success','votes':get_object_or_404(Suggestion, pk=spk).votes})

# 返回通知的具体信息
class JSONoticeDetial(View):
    def get(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        return JsonResponse({
            'level': notice.level,
            'content': notice.content,
            'create_time': f'{notice.create_time:%Y-%m-%d %H:%M:%S}',
        })
