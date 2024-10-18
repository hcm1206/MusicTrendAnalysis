"""
URL configuration for server project.

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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mainPage), # 루트(메인) 페이지
    path('test/', include('testapp.urls')), # 테스트 서브앱 루트 URL 설정
    path('chart/', include('chart.urls')), # 차트 앱 루트 URL 설정
    path('chartlist/', include('chartlist.urls')), # 차트리스트 앱 루트 URL 설정
    path('admin/', admin.site.urls),
]
