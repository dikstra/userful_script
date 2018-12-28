
import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite_env.settings'

if __name__ == '__main__':   

    subject, from_email = '测试邮件', 'hahnb@sina.com'
    to = ["zhoujiazheng@sunseaaiot.com"]
    text_content = 'test！'
    html_content = '<p>欢迎访问,this is a test mail！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()