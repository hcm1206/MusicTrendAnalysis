from django.shortcuts import render

# 테스트 메인 페이지 렌더링
def testapp(request):
    return render(request, 'testapp/testPage.html')
