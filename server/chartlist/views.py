from django.shortcuts import render
from django.http import Http404
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from keras.models import load_model
import pickle
from .models import TBL_MA

def chartlistPage(request, date):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    # data = pd.read_csv("../new_data/DBData.csv")
    # data = data[data["date"] == checkday.strftime('%Y-%m-%d')]
    # data = data[["Rank", "Title", "Artist"]]

    data = TBL_MA.objects.filter(Week_Date=checkday.strftime('%Y-%m-%d')).values("Week_Rank", "Title", "Artist")
    
    weekday_list = ['일', '월', '화', '수', '목', '금', '토']

    content = {
        'date' : checkday.strftime('%Y-%m-%d'),
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'weekday' : weekday_list[checkday.weekday()],
        'chart_data' : data,
    }

    return render(request, 'chartlist/chartlist.html', content)


def chartSongPage(request, date, rank):
    # ========== 날짜 설정 ==========
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    # ========== 데이터 확보 ==========

    data = pd.read_csv("../new_data/DBdata2410161600.csv", index_col=0) # DB 연동 시 이 부분을 DB와 통신하여 SQL 문으로 설정



    # ========== 모델 예측 결과 추출 ==========

    # input_data =  data[(data["date"] == checkday.strftime('%Y-%m-%d')) & (data["Rank"] == int(rank))][["Weekly Views", "n_score", "g_score", "Rank_lag_1", "Rank_lag_2", "Rank_lag_3"]]

    filter_data = TBL_MA.objects.get(Week_Date=checkday.strftime('%Y-%m-%d'), Week_Rank=int(rank))
    weekly_views = filter_data.Weekly_Views
    n_score = filter_data.n_score
    g_score = filter_data.g_score
    rank_lag_1 = filter_data.Rank_lag_1
    rank_lag_2 = filter_data.Rank_lag_2
    rank_lag_3 = filter_data.Rank_lag_3

    input_data = pd.DataFrame([[weekly_views, n_score, g_score, rank_lag_1, rank_lag_2, rank_lag_3]], columns=["Weekly Views", "n_score", "g_score", "Rank_lag_1", "Rank_lag_2", "Rank_lag_3"])

    with open('../new_data/scalers/views_scaler.pkl', 'rb') as f:
        views_scaler = pickle.load(f)
    with open('../new_data/scalers/n_score_scaler.pkl', 'rb') as f:
        n_score_scaler = pickle.load(f)
    with open('../new_data/scalers/g_score_scaler.pkl', 'rb') as f:
        g_score_scaler = pickle.load(f)

    input_data[["Weekly Views"]] = views_scaler.transform(input_data[["Weekly Views"]])
    input_data[["n_score"]] = n_score_scaler.transform(input_data[["n_score"]])
    input_data[["g_score"]] = g_score_scaler.transform(input_data[["g_score"]])
    
    input_data = input_data.to_numpy()
    input_data = np.reshape(input_data, (input_data.shape[0], 1, input_data.shape[1]))

    model = load_model('../modeling/lstm/lstm_model.keras')
    predicted_rank = int(model.predict(input_data)[0][0])

    # ========== 웹 페이지에 출력하기 위한 곡 정보 추출 ==========

    title = filter_data.Title
    artist = filter_data.Artist
    production = filter_data.Production
    genre = filter_data.Genre
    runtime = filter_data.Runtime

    # ========== 차트 출력을 위한  ==========

    prev_rank_list = []
    prev_date_list = []
    predicted_rank_list = []

    # =====================================================

    # date_now = checkday
    # week_cnt = 0

    # while datetime(year=2023, month=9, day=24) <= date_now and week_cnt <= 52:
    #     prev_date_list.append(date_now.strftime('%Y-%m-%d'))
    #     try:
    #         rank_now = data[(data["Title"] == title) & (data["Artist"] == artist) & (data["date"] == date_now.strftime('%Y-%m-%d'))][["Rank"]].iloc[0].values
    #         prev_rank_list.append(int(rank_now[0]))
    #     except IndexError as e:
    #         prev_rank_list.append(None)
    #     date_now -= timedelta(days=7)
    #     week_cnt += 1

    # prev_rank_list.reverse()
    # prev_date_list.reverse()

    # ====================================================

    date_now = datetime(year=2023, month=9, day=24)
    date_now = max(date_now, checkday - timedelta(weeks=52))
    chart_in = False

    min_rank = 201
    max_rank = 0

    while date_now <= checkday:
        try:
            rank_now = data[(data["Title"] == title) & (data["Artist"] == artist) & (data["date"] == date_now.strftime('%Y-%m-%d'))][["Rank"]].iloc[0].values
            min_rank = min(min_rank, int(rank_now[0]))
            max_rank = max(max_rank, int(rank_now[0]))
            prev_rank_list.append(int(rank_now[0]))
            prev_date_list.append(date_now.strftime('%Y-%m-%d'))
            if date_now == checkday:
                predicted_rank_list.append(predicted_rank)
            elif date_now == checkday - timedelta(days=7):
                predicted_rank_list.append(int(rank_now[0]))
            else:
                predicted_rank_list.append(None)
            chart_in = True
        except IndexError as e:
            if chart_in:
                prev_rank_list.append(None)
                prev_date_list.append(date_now.strftime('%Y-%m-%d'))
                predicted_rank_list.append(None)
        date_now += timedelta(days=7)

    min_rank = min(min_rank, predicted_rank)
    max_rank = max(max_rank, predicted_rank)

    # ====================================================
    

    prev_rank_list_json = json.dumps(prev_rank_list).replace('None', 'null')
    prev_date_list_json = json.dumps(prev_date_list).replace('None', 'null')
    predicted_rank_list_json = json.dumps(predicted_rank_list).replace('None', 'null')

    chart_length = len(prev_rank_list)



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
        'prev_rank_list' : prev_rank_list_json,
        'prev_date_list' : prev_date_list_json,
        'predicted_rank' : predicted_rank,
        'predicted_rank_list' : predicted_rank_list_json,
        'chart_length' : chart_length,
        'min_rank' : max((min_rank - 10) // 10 * 10, 0),
        'max_rank' : min((max_rank + 10) // 10 * 10, 200),
    }

    return render(request, 'chartlist/chartsong.html', content)
