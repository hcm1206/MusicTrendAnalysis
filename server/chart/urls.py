from django.urls import path, re_path
from . import views

app_name = "chartapp"

urlpatterns = [
    path("", views.chartPage), # 차트 메인 페이지
]