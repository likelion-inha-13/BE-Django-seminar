"""
URL configuration for seminar_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from util import views        # util 앱의 views.py 파일에서 뷰 함수들을 import

urlpatterns = [                # URL 패턴 목록을 담는 변수
    path('admin/', admin.site.urls), # 'admin/' URL로 시작하는 요청은 Django 관리자 페이지로 연결
    path('health/', views.health),  # 'health/' URL로 시작하는 요청은 util 앱의 views.py 파일에 있는 health 함수로 연결
]
