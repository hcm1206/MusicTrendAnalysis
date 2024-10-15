from django.shortcuts import render
from django.http import Http404
from datetime import datetime, timedelta
import pandas as pd

def chartlistPage(request, date):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    data = pd.read_csv("../data/final_total_data.csv", index_col=0)
    data = data[data["date"] == checkday.strftime('%Y-%m-%d')]
    data = data[["Rank", "Title", "New_Artist", "Production", "Genre"]]

    weekday_list = ['일', '월', '화', '수', '목', '금', '토']

    content = {
        'date' : checkday.strftime('%Y-%m-%d'),
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'weekday' : weekday_list[checkday.weekday()],
        'chart_data' : data.values.tolist(),
    }

    return render(request, 'chartlist/chartlist.html', content)


def chartSongPage(request, date, rank):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    content = {
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'rank' : rank,
    }

    return render(request, 'chartlist/chartsong.html', content)
