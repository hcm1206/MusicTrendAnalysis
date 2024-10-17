from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = "chartlistapp"

urlpatterns = [
    path("", RedirectView.as_view(url='2024-09-08')), # 차트리스트 메인 페이지
    re_path(r'^(\d{4}-\d{2}-\d{2})$', views.chartlistPage), # /(YYYY-MM-DD)형식에 해당하는 날짜 차트 라우팅
    re_path(r'^(\d{4}-\d{2}-\d{2})/([1-9][0-9]{0,1}|1[0-9]{2}|200)$', views.chartSongPage) # /(YYYY-MM-DD)/{랭킹} 해당하는 날짜 랭킹에 맞는 곡 페이지 라우팅
]
