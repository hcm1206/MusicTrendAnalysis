from django.shortcuts import render
from django.http import Http404
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from keras.models import load_model
import pickle

def chartlistPage(request, date):
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=9, day=24))

    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    data = pd.read_csv("../new_data/DBData.csv")
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

    data = pd.read_csv("../new_data/DBData.csv") # DB 연동 시 이 부분을 DB와 통신하여 SQL 문으로 설정

    # ========== 모델 예측 결과 추출 ==========

    input_data =  data[(data["date"] == checkday.strftime('%Y-%m-%d')) & (data["Rank"] == int(rank))][["Weekly Views", "n_score", "g_score", "Rank_lag_1", "Rank_lag_2", "Rank_lag_3"]]

    with open('../new_data/scalers/views_scaler.pkl', 'rb') as f:
        views_scaler = pickle.load(f)
    with open('../new_data/scalers/n_score_scaler.pkl', 'rb') as f:
        n_score_scaler = pickle.load(f)
    with open('../new_data/scalers/g_score_scaler.pkl', 'rb') as f:
        g_score_scaler = pickle.load(f)
    with open('../new_data/scalers/previous_rank_scaler.pkl', 'rb') as f:
        previous_rank_scaler = pickle.load(f)

    input_data[["Weekly Views"]] = views_scaler.transform(input_data[["Weekly Views"]])
    input_data[["n_score"]] = n_score_scaler.transform(input_data[["n_score"]])
    input_data[["g_score"]] = g_score_scaler.transform(input_data[["g_score"]])
    # input_data[["Rank_lag_1", "Rank_lag_2", "Rank_lag_3"]] = previous_rank_scaler.transform(input_data[["Rank_lag_1", "Rank_lag_2", "Rank_lag_3"]])
    
    input_data = input_data.to_numpy()
    input_data = np.reshape(input_data, (input_data.shape[0], 1, input_data.shape[1]))

    model = load_model('../modeling/lstm/lstm_model.keras')
    predicted_rank = int(model.predict(input_data)[0][0])

    # ========== 웹 페이지에 출력하기 위한 곡 정보 추출 ==========

    weekly_info = data[(data["date"] == checkday.strftime('%Y-%m-%d')) & (data["Rank"] == int(rank))].iloc[0].replace({np.nan: None})

    title = weekly_info["Title"]
    artist = weekly_info["Artist"]
    production = weekly_info["Production"]
    genre = weekly_info["Genre"]
    runtime = weekly_info["Runtime"]
    ky_rank = weekly_info["ky_rank"]

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

    while date_now <= checkday:
        
        try:
            rank_now = data[(data["Title"] == title) & (data["Artist"] == artist) & (data["date"] == date_now.strftime('%Y-%m-%d'))][["Rank"]].iloc[0].values
            prev_rank_list.append(int(rank_now[0]))
            prev_date_list.append(date_now.strftime('%Y-%m-%d'))
            if date_now == checkday:
            
            elif date_now == checkday - timedelta(days=7):
                predicted_rank_list.append(int(rank_now[0]))
            else:
                predicted_rank_list.append(None)
            chart_in = True
        except IndexError as e:
            if chart_in:
                prev_rank_list.append(None)
                prev_date_list.append(date_now.strftime('%Y-%m-%d'))
                predicted_rank_list(None)
        date_now += timedelta(days=7)

    # ====================================================
    

    prev_rank_list_json = json.dumps(prev_rank_list).replace('None', 'null')
    prev_date_list_json = json.dumps(prev_date_list).replace('None', 'null')




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
        'prev_rank_list' : prev_rank_list_json,
        'prev_date_list' : prev_date_list_json,
        'predicted_rank' : predicted_rank,
    }

    return render(request, 'chartlist/chartsong.html', content)
