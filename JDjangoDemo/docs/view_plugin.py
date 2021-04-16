from django.http import JsonResponse
from django.views.generic import View

from .models import LimitLinkPlugIn, PlugIn
from django.contrib.auth.models import User
from django.db.models import F

"""
    接口调用无需登录验证
"""

# 南京地铁
class NanJinMetro(View):
    ONLY_CODE = '0b81374e10644cb8b08882e212f4fc14' # 接口唯一码

    def get(self, request):
        # 硬性参数
        pid = request.GET.get('id', None)
        plicense = request.GET.get('license', None)
        # 根据pid获取合法用户
        user = User.objects.filter(other_info__token = pid)
        if len(user) > 0: # 用户存在
            user = user[0]
            # 根据接口唯一标识，获取接口实例
            try:
                # 接口和授权码存在
                plugin = PlugIn.objects.get(only_code = self.ONLY_CODE)
                obj = user.ulimits.filter(plugin = plugin)
            except:
                return JsonResponse({'msg': 'failure'})
            else:
                if len(obj) <= 0:
                    return JsonResponse({'msg': 'failure'})
                obj = obj[0]
                if obj.access_code == plicense:
                    # 判断是否还有剩余的调用次数
                    if obj.times <= 0:
                        return JsonResponse({'msg': 'failure'})
                    else:
                        # 剩余调用次数减一
                        obj.times = F('times') - 1
                        obj.save()
                        # 接口调用操作
                        # 接口参数
                        begin_station = request.GET.get('sstation', None)
                        end_station = request.GET.get('estation', None)
                        begin_line = request.GET.get('sline', None)
                        end_line = request.GET.get('eline', None)

                        from plugins.metro_tools import tools
                        all_lines = tools.get_all_ways(
                                begin_station = begin_station,
                                end_station = end_station,
                                begin_line = begin_line,
                                end_line = end_line
                            )[:]

                        return JsonResponse({
                            'msg': 'success',
                            'lines': all_lines,
                        })
                else:
                    pass
        else: # 用户不存在
            return JsonResponse({'msg': 'failure'})

            