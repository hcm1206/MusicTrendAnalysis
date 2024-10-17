from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
from keras.models import load_model
import pickle
from .models import TBL_MA

# 날짜 범위 조정 함수
def date_match(date : str) -> datetime:
    # 입력받은 날짜값 형식 무결성 체크
    try:
        checkday = datetime.strptime(date, '%Y-%m-%d')
    except:
        raise Http404("Invalid Date; 날짜 형식이 올바르지 않습니다.")
    
    # 날짜가 데이터 수집 범위인 2023년 10월 15일(9월 24일의 3주 후)부터 2024년 9월 8일 사이의 범위를 갖도록 조정
    checkday = min(checkday, datetime(year=2024, month=9, day=8))
    checkday = max(checkday, datetime(year=2023, month=10, day=15))

    # 해당 날짜의 가장 최근 일요일로 조정
    while checkday.weekday() < 6:
        checkday -= timedelta(days=1)

    return checkday

# 차트 목록 페이지 뷰 함수
def chartlistPage(request, date):
    # 차트에 유효한 일요일 날짜로 변경(2023.10.15 ~ 2024.9.8 사이 일요일)
    checkday = date_match(date)

    # CSV를 이용하여 해당되는 날짜 차트 리스트 데이터 로드(비활성화)
    # data = pd.read_csv("../new_data/DBData.csv")
    # data = data[data["date"] == checkday.strftime('%Y-%m-%d')]
    # data = data[["Rank", "Title", "Artist"]]

    # 데이터베이스를 이용하여 해당되는 날짜 리스트 데이터 로드
    data = TBL_MA.objects.filter(Week_Date=checkday.strftime('%Y-%m-%d')).values("Week_Rank", "Title", "Artist")
    
    # 요일 출력을 위한 배열 생성
    weekday_list = ['일', '월', '화', '수', '목', '금', '토']

    # 전송할 데이터 묶음
    content = {
        'date' : checkday.strftime('%Y-%m-%d'),
        'year' : checkday.year,
        'month' : checkday.month,
        'day' : checkday.day,
        'weekday' : weekday_list[checkday.weekday()],
        'chart_data' : data,
    }

    # chartlist.html 렌더링
    return render(request, 'chartlist/chartlist.html', content)

# 날짜와 랭킹에 해당하는 곡 세부 정보 페이지 뷰 함수
def chartSongPage(request, date, rank):
    # ========== 날짜 설정 ==========

    # 차트에 유효한 일요일 날짜로 변경(2023.10.15 ~ 2024.9.8 사이 일요일)
    checkday = date_match(date)

    # ========== 데이터 확보 ==========

    # CSV를 이용하여 해당되는 날짜 차트 리스트 데이터 로드(비활성화)
    # data = pd.read_csv("../new_data/DBdata2410161600.csv", index_col=0)

    # 입력된 날짜와 랭크에 해당하는 곡 정보를 DB에서 추출
    filter_data = TBL_MA.objects.get(Week_Date=checkday.strftime('%Y-%m-%d'), Week_Rank=int(rank))
    weekly_views = filter_data.Weekly_Views
    n_score = filter_data.n_score
    g_score = filter_data.g_score
    rank_lag_1 = filter_data.Rank_lag_1
    rank_lag_2 = filter_data.Rank_lag_2
    rank_lag_3 = filter_data.Rank_lag_3

    # ========== 모델 예측 결과 추출 ==========

    # CSV 이용 시 데이터프레임 필터링(비활성화)
    # input_data =  data[(data["date"] == checkday.strftime('%Y-%m-%d')) & (data["Rank"] == int(rank))][["Weekly Views", "n_score", "g_score", "Rank_lag_1", "Rank_lag_2", "Rank_lag_3"]]

    # 추출된 데이터를 데이터프레임 형태로 변환
    input_data = pd.DataFrame([[weekly_views, n_score, g_score, rank_lag_1, rank_lag_2, rank_lag_3]], columns=["Weekly Views", "n_score", "g_score", "Rank_lag_1", "Rank_lag_2", "Rank_lag_3"])

    # 피처 데이터를 스케일링하기 위한 스케일러 로드
    with open('../new_data/scalers/views_scaler.pkl', 'rb') as f:
        views_scaler = pickle.load(f)
    with open('../new_data/scalers/n_score_scaler.pkl', 'rb') as f:
        n_score_scaler = pickle.load(f)
    with open('../new_data/scalers/g_score_scaler.pkl', 'rb') as f:
        g_score_scaler = pickle.load(f)

    # 데이터 스케일링
    input_data[["Weekly Views"]] = views_scaler.transform(input_data[["Weekly Views"]])
    input_data[["n_score"]] = n_score_scaler.transform(input_data[["n_score"]])
    input_data[["g_score"]] = g_score_scaler.transform(input_data[["g_score"]])
    
    # keras 모델 입력 형식에 맞게 변환
    input_data = input_data.to_numpy()
    input_data = np.reshape(input_data, (input_data.shape[0], 1, input_data.shape[1]))

    # 학습된 keras 모델 로드
    model = load_model('../modeling/lstm/lstm_model.keras')
    # 모델에 데이터 입력하여 예측값 생성
    predicted_rank = int(model.predict(input_data)[0][0])

    # ========== 웹 페이지에 출력하기 위한 곡 정보 추출 ==========

    # 각 데이터 정보를 추출
    title = filter_data.Title
    artist = filter_data.Artist
    production = filter_data.Production
    genre = filter_data.Genre
    runtime = filter_data.Runtime

    # ========== 차트 출력을 위한 리스트 생성 ==========

    prev_rank_list = [] # 역대 차트 랭킹 저장할 리스트
    prev_date_list = [] # 차트 랭킹과 매칭되는 날짜 문자열 저장할 리스트
    predicted_rank_list = [] # 차트 랭킹과 매칭되는 예측값 저장할 리스트(1주전 랭크와 이번주 랭크 예측 값 제외하고 None으로 저장)

    # =====================================================

    # 랭킹 수집 시작 날짜 생성(2023년 9월 24일 또는 현재 시점으로부터 52주(약 1년) 전)
    date_now = datetime(year=2023, month=9, day=24)
    date_now = max(date_now, checkday - timedelta(weeks=52))
    chart_in = False # 발매 여부를 확인하기 위한 플래그 변수

    # 곡의 랭크 최소최대값 체크
    min_rank = 201
    max_rank = 0

    # 시작 날짜부터 현재 날짜까지 일주일 단위로 체크
    while date_now <= checkday:
        # 이번 주에 곡 랭크 정보가 있다면
        try:
            # 이번 주 곡의 랭크를 추출하여 리스트에 저장
            rank_now = TBL_MA.objects.get(Week_Date=date_now.strftime('%Y-%m-%d'), Title=title, Artist=artist).Week_Rank
            min_rank = min(min_rank, rank_now)
            max_rank = max(max_rank, rank_now)
            prev_rank_list.append(rank_now)
            prev_date_list.append(date_now.strftime('%Y-%m-%d'))
            if date_now == checkday:
                predicted_rank_list.append(predicted_rank)
            elif date_now == checkday - timedelta(days=7):
                predicted_rank_list.append(rank_now)
            else:
                predicted_rank_list.append(None)
            chart_in = True
        # 이번 주에 곡 랭크 정보가 없다면
        except ObjectDoesNotExist as e:
            # 만약 이전에 200위 안에 들었던 내역이 있으면 리스트에 None을 넣음
            if chart_in:
                prev_rank_list.append(None)
                prev_date_list.append(date_now.strftime('%Y-%m-%d'))
                predicted_rank_list.append(None)
            # 이전에 200위 내역이 없으면 신곡 또는 역주행 곡으로 리스트를 채우지 않고 그대로 진행
        date_now += timedelta(days=7)

    min_rank = min(min_rank, predicted_rank)
    max_rank = max(max_rank, predicted_rank)

    # ====================================================
    
    # 생성한 리스트들을 자바스크립트에서 사용하기 위해 JSON 형식으로 변환
    prev_rank_list_json = json.dumps(prev_rank_list).replace('None', 'null')
    prev_date_list_json = json.dumps(prev_date_list).replace('None', 'null')
    predicted_rank_list_json = json.dumps(predicted_rank_list).replace('None', 'null')

    # 랭크 리스트 길이(차트인 했던 횟수) 저장
    chart_length = len(prev_rank_list)

    # 전송할 데이터 묶음
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

    # chartsong.html 렌더링
    return render(request, 'chartlist/chartsong.html', content)
