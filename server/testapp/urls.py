from django.urls import path, re_path
from . import views

app_name = "testapp"

urlpatterns = [
    path("", views.testapp), # 테스트 메인 페이지
]