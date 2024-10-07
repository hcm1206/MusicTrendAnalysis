from django.shortcuts import render

import random
import json

# 차트 테스트 페이지 렌더링
def chartPage(request):

    # =================== 랜덤 시계열 순위 데이터 생성 코드 ===================
    # 계산할 주의 개수 설정
    WEEK = 52
    # 과거 52주 데이터 저장할 리스트 생성
    random_list = []
    # 미래 53주 데이터 예측값 저장할 리스트 생성
    predicted_list = []
    # 먼저 1주차에 시작할 차트 순위 랜덤 생성(1위 ~ 110위)
    now = random.randint(1, 110)
    # 현재 순위에서 -20 ~ 20 사이 값을 더하는 과정을 반복하여 1년치 시계열 데이터 생성
    for i in range(WEEK):
        # ==== 과거 데이터 입력 ====
        if now <= 100:
            random_list.append(max(1, now)) # 최대 순위는 1위
        # 현재 순위가 100위 밖으로 벗어나면 None(결측치) 처리
        else:
            random_list.append(None)
        # ==== 예측 데이터 입력 ====
        # 가장 최근(52주차)가 아니면 모두 None을 입력
        if i < WEEK - 1:
            predicted_list.append(None)
        # 가장 최근 데이터이고 1~100위 범위 내라면 예측 리스트에 가장 최근 데이터 입력
        else:
            if now <= 100:
                predicted_list.append(max(1, now))
            else:
                predicted_list.append(None)
        # ==== 데이터 갱신 ====
        now = max(-10, now + random.randint(-20, 20))
    # 과거 데이터 다 채웠으면 이제 다음 주차 예측값을 설정할 차례
    # 과거 데이터에 들어가는 리스트의 마지막은 None으로 설정
    random_list.append(None)
    # 예측 순위가 1~100위이면 예측 리스트에 예측 순위 입력
    if (now <= 100):
        predicted_list.append(max(1, now))
    else:
        predicted_list.append(None) 

    # 최종적으로 
    # 과거 리스트는 [10, 15, 13, ..., 84, 90, None]처럼 될 것이고
    # 예측 리스트는 [None, None, None, ..., None, 90, 96]처럼 될 것
    # 이 두 가지 데이터를 차트에 그리면 하나의 데이터처럼 보이게 됨

    # 자바스크립트에서 처리할 수 있도록 리스트를 JSON 형식으로 바꾸고 결측치 None을 JSON에서 쓰이는 null로 변경
    random_list_json = json.dumps(random_list).replace('None', 'null')
    predicted_list_json = json.dumps(predicted_list).replace('None', 'null')

    # 현재 순위와 예측 순위 저장
    present_rank = predicted_list[-2]
    predicted_rank = predicted_list[-1]

    # 그냥 차트 밑에 띄울 텍스트 설정
    ment = "다음 순위 예측 : "
    if (predicted_rank):
        ment += f"{predicted_rank}위"
    else:
        ment += "100위권 밖"

    content = {
        'list' : random_list_json,
        'predicted_list' : predicted_list_json,
        'ment' : ment,
    }
    return render(request, 'chart/chart.html', content)