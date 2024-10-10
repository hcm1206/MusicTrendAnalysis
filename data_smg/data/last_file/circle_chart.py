from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta

# 데이터를 저장할 리스트 초기화
ranks = []
titles = []
artists = []
productions = []
start_dates = []

# User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}

# 2023년 1주차부터 2024년 37주차까지 반복
for year in [2023, 2024]:
    for week in range(1, 53 if year == 2023 else 38):
        # 웹페이지 URL 생성
        url = f"https://circlechart.kr/page_chart/onoff.circle?nationGbn=T&serviceGbn=ALL&targetTime={week}&hitYear={year}&termGbn=week&yearTime=3"

        # HTTP 요청을 보내고 페이지 내용을 가져옴
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        tbody = soup.find('tbody', id='pc_chart_tbody')

        # 각 주차의 시작 날짜 계산 (월요일)
        start_date = datetime(year, 1, 1) + timedelta(weeks=week - 1)
        start_dates.append(start_date.strftime('%Y-%m-%d'))

        if tbody:
            for row in tbody.select('tr'):
                try:
                    rank_elem = row.select_one('td:nth-child(1) > div > span')
                    title_elem = row.select_one('td:nth-child(3) > div > section:nth-child(2) > div > div.font-bold.mb-2')
                    artist_elem = row.select_one('td:nth-child(3) > div > section:nth-child(2) > div > div.text-sm.text-gray-400.font-bold')
                    production_elem = row.select_one('td.text-left.text-xs > div:nth-child(1) > span')

                    # 각 요소가 존재하는지 확인 후 텍스트 추출
                    rank = rank_elem.text.strip() if rank_elem else None
                    title = title_elem.text.strip() if title_elem else None
                    if artist_elem:
                        full_text = artist_elem.text.strip()
                        artist = full_text.split(' |')[0].strip()
                    else:
                        artist = None
                    production = production_elem.text.strip() if production_elem else None

                    # 리스트에 데이터 추가
                    ranks.append(rank)
                    titles.append(title)
                    artists.append(artist)
                    productions.append(production)
                except AttributeError as e:
                    print(f"Error: {e}")
                    continue
        else:
            print(f"No tbody found for {year} week {week}")

# 모든 데이터를 pandas DataFrame으로 변환
df = pd.DataFrame({
    'Start Date': start_dates,
    'Rank': ranks,
    'Title': titles,
    'Artist': artists,
    'Production': productions
})

# 데이터프레임을 CSV 파일로 저장
df.to_csv('circle_chart_data_with_dates.csv', index=False, encoding='utf-8-sig')

# 데이터프레임 출력
print("데이터 수집 완료")
print(df)
