from django.shortcuts import render
from django.http import Http404
from datetime import datetime, timedelta

def chartlistPage(request, date):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    print(checkday.weekday())

    while checkday.weekday() > 0:
        checkday -= timedelta(days=1)

    weekday_list = ['일', '월', '화', '수', '목', '금', '토']

    content = {
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'weekday' : weekday_list[checkday.weekday()],
    }

    return render(request, 'chartlist/chartlist.html', content)
