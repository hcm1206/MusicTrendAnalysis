from django.shortcuts import render
from django.http import HttpResponse

# 메인페이지 렌더링
def mainPage(request):
    return render(request, 'mainPage.html') 