import time
from pytrends.request import TrendReq
import pandas as pd
import re
from pytrends.exceptions import ResponseError

# CSV 파일에서 아티스트 데이터 로드
artists = pd.read_csv(r"C:\Users\user\Desktop\testproject\unique_title_artist.csv")

# 특수기호, 영어, 한글 처리 로직
def clean_korean_name(name):
    # 한글만 포함하는 경우: 특수기호와 영어 제거
    korean_only = re.sub(r'[^가-힣\s]', '', name)
    # 영어만 포함하는 경우: 그대로 유지
    if not korean_only.strip():  # 한글이 없으면
        return name.strip()  # 영어 그대로 반환
    return korean_only.strip()

# 변환한 이름 저장
artists['변환한이름'] = artists['Artist'].apply(clean_korean_name)

# Pytrends 초기화
pytrends = TrendReq(hl='ko', tz=360)

# 아티스트 이름 리스트로 변환
cleaned_artist_names = artists['변환한이름'].unique().tolist()

# 트렌드 결과를 저장할 데이터프레임 준비
all_trends = pd.DataFrame()

# Google 트렌드 검색을 5개씩 묶어 실행
batch_size = 5
for i in range(0, 10, batch_size):
    batch = cleaned_artist_names[i:i + batch_size]
    
    # 이름이 비어있지 않은 경우만 처리
    batch = [name for name in batch if name]
    
    try:
        pytrends.build_payload(kw_list=batch, timeframe='today 12-m', geo='KR')
        
        interest_over_time = pytrends.interest_over_time()
        # 인덱스를 열로 변환
        interest_over_time = interest_over_time.reset_index()
        # print(interest_over_time.columns)
        if not interest_over_time.empty:
            # 날짜 열을 Label로, 각 날짜의 점수를 해당 날짜의 데이터로 설정
            for keyword in batch:
                keyword_trends = interest_over_time[['date', keyword]].copy()
                keyword_trends['변환한이름'] = keyword
                keyword_trends.rename(columns={keyword: 'Score'}, inplace=True)
                all_trends = pd.concat([all_trends, keyword_trends], axis=0)  # 행으로 추가
    
    except ResponseError as e:
        print(f"Error: {e}. 60초 동안 대기합니다.")
        time.sleep(60)
    
    # 요청 사이에 30초 대기
    time.sleep(30)

# 트렌드 데이터를 아티스트 데이터와 병합하기 위해 아티스트 기준으로 병합
final_data = pd.merge(artists, all_trends, how='left', left_on='변환한이름', right_on='변환한이름')

# 최종 데이터 저장
final_data.to_csv('artist_trends_31.csv', index=False)

print("트렌드 데이터가 성공적으로 추가되었습니다!")
