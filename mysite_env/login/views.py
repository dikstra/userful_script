import datetime
import hashlib
import random
from django.shortcuts import render,HttpResponseRedirect
from django.shortcuts import redirect
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from login import models,forms
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site


def hash_code(s,salt=None):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def set_salt():
    return ''.join([chr(random.randint(48, 122)) for i in range(20)])

def login(request):
    hashkey = CaptchaStore.generate_key()
    imgage_url = captcha_image_url(hashkey)

    if request.method == "GET":
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/autoplat/')
        if request.session.get('is_login',None):
            return redirect("/autoplat/")

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户还未通过邮箱确认！'
                    return render(request,'login/login.html',locals())
                salt = user.salt
                if user.password == hash_code(password,salt):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_permission'] = user.admin
                    return HttpResponseRedirect(request.session['login_from'])
                    #return render(request,'login/index.html')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect("/autoplat/")
    if request.method ==  "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "2次输入的密码不一致"
                return render(request,'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message="用户已经存在，请重新选择用户名"
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                current_site = get_current_site(request)
                domain=current_site.domain
                new_user = models.User()
                salt = set_salt()
                new_user.name = username
                new_user.salt = salt
                new_user.password = hash_code(password1, salt)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email,code,domain,username)

                message = '请前往注册邮箱，进行邮箱确认！'
                return render(request, 'login/confirm.html', locals())
        return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def forgot_password(request):
    if request.session.get('is_login',None):
        return redirect("/autoplat/")
    if request.method ==  "POST":
        resetpassword_form = forms.ResetPassword(request.POST)
        message = "请检查填写内容"
        if resetpassword_form.is_valid():
            username = resetpassword_form.cleaned_data['username']
            password1 = resetpassword_form.cleaned_data['password1']
            password2 = resetpassword_form.cleaned_data['password2']
            if password1 != password2:
                message = "2次输入的密码不一致"
                return render(request, 'login/forgot_password.html', locals())
            else:
                name_user = models.User.objects.filter(name=username)
                if name_user:
                    salt = set_salt()
                    password = hash_code(password1,salt)
                    name_user.update(password=password,salt=salt)
                    message = '密码修改成功！即将跳转至登陆页面'
                    return render(request, 'login/password_confirm.html', locals())

                else:
                    message = "用户名不存在，请重新输入"
                    return render(request, 'login/forgot_password.html', locals())
    resetpassword_form = forms.ResetPassword(request.POST)
    return render(request, 'login/forgot_password.html', locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/autoplat/")
    request.session.flush()
    return redirect('/autoplat/')

def user_confirm(request):
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request,'login/confirm.html',locals())
    c_time = confirm.c_time
    now = timezone.now()
    # now = datetime.datetime.now() 该时间获取没有时区
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        message = '您的邮箱已经过期！请重新注册！'
        return render(request,'login/confirm.html',locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账号登录！'
        return render(request,'login/confirm.html',locals())


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name,now)
    models.ConfirmString.objects.create(code=code,user=user,)
    return code

def send_email(email,code,domain,username):
    subject = '来自日海物联网站的注册确认邮箱'
    text_content = "感谢注册日海物联运维系统，如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！"
    html_content = '''
                    <p> Hi {} </p>
                    <p>感谢日海物联运维系统注册<a href="http://{}/confirm/?code={}" target=blank>www.sunseaaiot.com</a>,\
                    日海物联运维系统提供强大的运维监控功能！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(username,domain, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()