from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time


# 创建Celery实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(email_to, username, token):
    """发送邮件"""
    subject = '天天生鲜'
    message = ''
    sender = settings.EMAIL_FROM
    reciver = [email_to]
    msg = '<h1>%s,天天生鲜欢迎您！</h1><span>请点击以下链接进行用户激活：</span><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, reciver, html_message=msg)
    time.sleep(5)