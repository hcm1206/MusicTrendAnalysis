from django.shortcuts import render
from django.http import HttpResponse
import csv
from .models import TBL_MA # '고객' 테이블에 해당하는 모델을 불러옵니다.
from io import StringIO
from django.core.paginator import Paginator

# 테스트 메인 페이지 렌더링
def testapp(request):
    return render(request, 'testapp/testPage.html')

# def export_to_csv(request):
#     # # CSV 파일을 HTTP 응답으로 반환 (Content-Type 지정)
#     # response = HttpResponse(content_type='text/csv')
#     # response['Content-Disposition'] = 'attachment; filename="고객_data_export.csv"'
#     csv_file = StringIO()
#     writer = csv.writer(csv_file)
    
#     # CSV 작성자 생성
#     # writer = csv.writer(response)
    
#     # CSV 파일의 헤더 작성 (필드 이름들)
#     writer.writerow(['고객번호', '고객회사명', '담당자명', '담당자직위', '주소', '도시', '지역', '전화번호', '마일리지'])  # 실제 모델 필드 이름으로 변경
    
#     # 데이터베이스에서 모든 데이터 조회
#     for obj in 고객.objects.all().values_list('고객번호', '고객회사명', '담당자명', '담당자직위', '주소', '도시', '지역', '전화번호', '마일리지'):  # 필드 이름 맞게 변경
#         writer.writerow(obj)
    
#     csv_file.seek(0)
#     reader = csv.reader(csv_file)

#     return render(request, 'testapp/testPage.html', {'csv_data': reader})

# def test_view(request):
#     고객_목록 = 고객.objects.all()
#     for 고객_데이터 in 고객_목록:
#         print(고객_데이터.name, 고객_데이터.email)
#     return HttpResponse("Success")

# def import_csv_to_db(request):
#     # CSV 데이터 받아오기 (여기서는 메모리에서 가져옴, 실제로는 업로드한 파일에서 가져옴)







#     csv_content = request.POST.get('csv_content')
#     csv_file = StringIO(csv_content)
#     reader = csv.reader(csv_file)

#     next(reader)  # 첫 번째 줄(헤더) 건너뛰기
    
#     # CSV 데이터를 데이터베이스에 저장
#     for row in reader:
#         고객.objects.create(
#             고객번호=row[0],
#             고객회사명=row[1],
#             담당자명=row[2],
#             담당자직위=row[3],
#             주소=row[4],
#             도시=row[5],
#             지역=row[6],
#             전화번호=row[7],
#             마일리지=row[8]
#         )
    
#     return HttpResponse("CSV 데이터가 성공적으로 MySQL에 저장되었습니다.")


# def customer_list(request):

#     # MySQL '고객' 테이블의 모든 데이터를 조회
#     customer_data = 고객.objects.all()

#     # Paginator 객체를 사용해 한 페이지에 100개의 항목을 표시
#     paginator = Paginator(customer_data, 100)  # 페이지당 100개의 항목
#     page_number = request.GET.get('page')  # 현재 페이지 번호를 GET 파라미터로 받음
#     page_obj = paginator.get_page(page_number)  # 현재 페이지의 데이터를 가져옴

#     # 데이터를 템플릿으로 전달
#     return render(request, 'testapp/customer_list.html', {'page_obj': page_obj})

def tbl_ma_list(request):
    # MySQL 'TBL_MA' 테이블의 모든 데이터를 조회
    ma_data = TBL_MA.objects.all().order_by('Week_Date', 'Week_Rank')

    # Paginator 객체를 사용해 한 페이지에 100개의 항목을 표시
    paginator = Paginator(ma_data, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 데이터를 템플릿으로 전달
    return render(request, 'testapp/tbl_ma_list.html', {'page_obj': page_obj})

