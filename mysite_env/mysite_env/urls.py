"""mysite_env URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^autoplat/',include('autoplat.urls')),
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^login/',views.login, name='login'),
    url(r'^register/',views.register),
    url(r'^forgot_password/',views.forgot_password, name='forgot_passowrd'),
    url(r'^logout/',views.logout),
    url(r'^confirm/$',views.user_confirm),
    url(r'^captcha',include('captcha.urls'))
]
