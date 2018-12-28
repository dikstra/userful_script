from django.shortcuts import render,redirect,HttpResponse
from autoplat import forms
from login import models
from autoplat import models as Bmodels
# Create your views here.

def login_check(func):
    def check(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')
    return check

@login_check
def asset_add(request,detail_id):
    if request.method == "POST":
        a_form = AssetForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            messages = u"增加成功！"
            display_control = ""
        else:
            messages = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/asset_add.html", locals())
    else:
        display_control = "none"
        a_form = AssetForm()
        return render(request, "cmdb/asset_add.html", locals())

