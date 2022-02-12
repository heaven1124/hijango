"""hidjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.conf.urls.static import static


# 声明views处理函数
def index(request: HttpRequest):
    users = [{'id': 1, 'name': 'sl'},
             {'id': 2, 'name': 'zh'},
             {'id': 3, 'name': 'wj'},
            ]
    # return HttpResponse('<h1>hi, django</h1>'.encode('utf-8'))
    return render(request, 'index.html', {'users': users, 'msg': 'all msgs'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    # 配置子路由，include导入urls.py中所有子路由
    path('user/', include('mainapp.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
