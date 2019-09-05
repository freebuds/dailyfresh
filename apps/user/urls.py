from django.conf.urls import url
from user.views import RegisterView, UserActive, LoginView

urlpatterns = [
    # url(r'^register$', views.register, name='register'), # 注册页面
    url(r'^register$', RegisterView.as_view(), name='register'),  # 用户注册页面
    url(r'^active/(?P<token>.*)$', UserActive.as_view(), name='active'),  # 用户激活链接
    url(r'^login$', LoginView.as_view(), name='login'),  # 登陆页面
 ]
