from django.urls import path, re_path
from . import views

app_name = "testapp"

urlpatterns = [
    path("", views.tbl_ma_list, name='tbl_ma_list'), # 테스트 메인 페이지
    #path('export_csv/', views.export_to_csv, name='export_to_csv'), #CSV 내보내기 URL추가
    #path('import_csv_to_db/', views.import_csv_to_db, name='import_csv_to_db'),  # CSV 데이터를 MySQL에 저장하는 URL 추가
    #path('customerweb/', views.customer_list, name='customer_list'), #'고객' 데이터를 보여주는 URL
    path('tbl_ma/', views.tbl_ma_list, name='tbl_ma_list'),

]
