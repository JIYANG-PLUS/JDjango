from django.db import models
from django.db.models import Q,F
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

class ArticleManage(models.Manager):
    # 近一周发表的文章
    @property
    def duringWeekA(self):
        now = datetime.now()
        return self.filter(create_time__range=(now-timedelta(days=7), now))

    # 近半月发表的文章
    @property
    def duringHalfMonthA(self):
        now = datetime.now()
        return self.filter(create_time__range=(now-timedelta(days=15), now))

    # 近一月发表的文章
    @property
    def duringMonthA(self):
        now = datetime.now()
        return self.filter(create_time__range=(now-timedelta(days=30), now))

    # 近半年发表的文章
    @property
    def duringHalfYearA(self):
        now = datetime.now()
        return self.filter(create_time__range=(now-timedelta(days=180), now))

    # 取精选文章
    @property
    def goodChoiceArticles(self):
        return self.filter(isgood=True).order_by('-votes') #根据支持率进行排序

class RemarkManage(models.Manager):
    pass

class SuggestVoteManage(models.Manager):
    # 接收投票人对象和建议对象，并进行绑定投票
    def vote(self, user, suggest):
        # 检测投票对象是否存在
        if len(self.filter(voter=user)) > 0:
            return False # 已投票，投票失败
        else:
            # 创建投票对象
            obj = self.create(isvote=True,voter=user,suggest=suggest)
            # 投票数加一
            suggest.votes = F('votes') + 1
            suggest.save()
            return True # 投票成功
 