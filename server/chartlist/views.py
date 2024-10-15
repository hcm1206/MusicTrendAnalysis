from django.shortcuts import render
from django.http import Http404
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json

def chartlistPage(request, date):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    data = pd.read_csv("../modeling/00_projectx/test/circle_chart_with_trends(20241002).csv")
    data = data[data["date"] == checkday.strftime('%Y-%m-%d')]
    data = data[["Rank", "Title", "Artist"]]

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

    data = pd.read_csv("../modeling/00_projectx/test/circle_chart_with_trends(20241002).csv")

    weekly_info = data[(data["date"] == checkday.strftime('%Y-%m-%d')) & (data["Rank"] == int(rank))].iloc[0].replace({np.nan: None})

    title = weekly_info["Title"]
    artist = weekly_info["Artist"]
    production = weekly_info["Production"]
    genre = weekly_info["Genre"]
    runtime = weekly_info["Runtime"]
    ky_rank = weekly_info["ky_rank"]

    prev_rank_list = []
    prev_date_list = []

    date_now = checkday
    week_cnt = 0

    while datetime(year=2023, month=9, day=24) <= date_now and week_cnt <= 52:
        prev_date_list.append(date_now.strftime('%Y-%m-%d'))
        rank_now = data[(data["Title"] == title) & (data["Artist"] == artist) & (data["date"] == date_now.strftime('%Y-%m-%d'))][["Rank"]].iloc[0].values
        prev_rank_list.append(rank_now)
        week_cnt += 1

    print(prev_rank_list)
    print(prev_date_list)
    prev_ranks = data[(data["Title"] == title) & (data["Artist"] == artist)][["date", "Rank"]]
    prev_ranks_list = prev_ranks.to_numpy().tolist()
    prev_ranks_list_json = json.dumps(prev_ranks_list).replace('None', 'null')

    content = {
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'rank' : rank,
        'title' : title,
        'artist' : artist,
        'production' : production,
        'genre' : genre,
        'runtime' : runtime,
        'ky_rank' : ky_rank,
        'ranks' : prev_ranks_list_json,
    }

    return render(request, 'chartlist/chartsong.html', content)
