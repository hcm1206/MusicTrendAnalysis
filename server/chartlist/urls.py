from django.urls import path, re_path
from django.views.generic import RedirectView
from datetime import datetime
from . import views

app_name = "chartlistapp"

urlpatterns = [
    path("", RedirectView.as_view(url='2024-09-08')), # 차트리스트 메인 페이지
    re_path(r'^(\d{4}-\d{2}-\d{2})$', views.chartlistPage),
    re_path(r'^(\d{4}-\d{2}-\d{2})/([1-9][0-9]{0,1}|1[0-9]{2}|200)$', views.chartSongPage)
]
