from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.views.generic import View
from celery_tasks.tasks import send_register_active_email
from user.models import User
import re
import time

# Create your views here.

# /user/register
# def register(request):
#     """注册页面"""
#     return render(request, 'register.html')
# 类视图
class RegisterView(View):
    """注册页面"""
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        """注册校验"""
        # 接收数据
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据处理
        if not all([username, pwd, email]):
            return render(request, 'register.html', {'error_msg': '数据不完整'})

        # 查询用户名是否重复，捕获到异常说明用户名不存在，否则用户名存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'error_msg': '用户名已存在'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'error_msg': '邮箱格式错误'})

        if allow != 'on':
            return render(request, 'register.html', {'error_msg': '请同意协议'})
        # 业务处理
        user = User.objects.create_user(username, email, pwd)
        user.is_active = 0
        user.save()

        # 发送邮件，包含激活链接  http://127.0.0.1:8000/user/active/id(加密后的id)
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        res = serializer.dumps(info)
        token = res.decode()
        print('http://127.0.0.1:8000/user/active/%s' % token)

        # 发送邮件
        send_register_active_email.delay(email, username, token)

        # 返回应答
        return redirect(reverse('goods:index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class UserActive(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            res = serializer.loads(token)
        except:
            # 实际项目应该跳转到某个页面，然后从新发激活链接
            return HttpResponse('激活链接已经过期')
        user_id = res['confirm']
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()
        return redirect(reverse('user:login'))