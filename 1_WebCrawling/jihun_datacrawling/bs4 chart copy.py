import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import timedelta, datetime

# 기준 주차와 일요일 날짜 설정
base_week_seq = 1348
base_week_date = datetime(2024, 9, 8)  # 기준 일요일 날짜

# 크롤링할 URL 리스트 생성 (주차 범위 및 페이지 범위에 맞게 생성)
base_url = "https://kysing.kr/popular/?period=w&songweekseq={}&range={}"

# songweekseq 값은 범위에 맞게 설정
week_range = range(1286, 1349)  # 1286부터 1348까지
page_range = [1, 2]  # 1~50위 페이지, 51~100위 페이지

# 크롤링한 데이터 저장할 리스트
data = []

# 주차별 일요일 날짜 자동 계산 함수
def get_week_date(week_seq):
    week_diff = base_week_seq - week_seq
    return base_week_date - timedelta(weeks=week_diff)

# 크롤링 함수
def crawl_chart(week_seq, page):
    url = base_url.format(week_seq, page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 순위, 곡명, 가수 크롤링
    for i in range(2, 52):  # 1위부터 50위까지
        rank_selector = f'#popular_chart_frm > div > ul:nth-child({i}) > li.popular_chart_chk > label > span.popular_chart_link'
        song_selector = f'#popular_chart_frm > div > ul:nth-child({i}) > li.popular_chart_tit.clear > span:nth-child(1)'
        singer_selector = f'#popular_chart_frm > div > ul:nth-child({i}) > li.popular_chart_sng'

        rank = soup.select_one(rank_selector)
        song = soup.select_one(song_selector)
        singer = soup.select_one(singer_selector)

        if rank and song and singer:
            data.append({
                'date': get_week_date(week_seq).strftime('%Y-%m-%d'),
                'rank': rank.text.strip(),
                'song': song.text.strip(),
                'singer': singer.text.strip()
            })

# 주차별, 페이지별로 데이터를 크롤링
for week_seq in week_range:
    for page in page_range:
        crawl_chart(week_seq, page)

# 데이터프레임으로 변환
df = pd.DataFrame(data)

# 결과 출력
print(df)

# 원하는 파일로 저장 (CSV 파일로 저장 가능)
df.to_csv('ky_singing_popular_chart.csv', index=False)
