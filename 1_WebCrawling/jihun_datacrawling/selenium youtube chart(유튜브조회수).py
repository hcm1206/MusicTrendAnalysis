from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime, timedelta

# ChromeDriver 경로 설정
chrome_driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'

# Service 객체 생성
service = Service(executable_path=chrome_driver_path)

# 브라우저 열기 (Service 객체를 통해)
driver = webdriver.Chrome(service=service)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 10)

# 아티스트 이름과 조회수를 담을 리스트
artists_data = []

# 시작일 설정 (오늘 날짜를 기준으로 지난 52주 계산)
current_date = datetime(2024, 9, 19)

# 52주 동안의 데이터를 수집
for week in range(52):
    # 주간 URL 설정 (current_date의 날짜를 차트 URL에 맞게 포맷)
    week_start_date = current_date.strftime('%Y%m%d')  # 20240919 형식으로 변환
    url = f'https://charts.youtube.com/charts/TopArtists/kr/weekly/{week_start_date}'
    print(f"Fetching data for week starting: {week_start_date}")

    # 해당 URL 열기
    driver.get(url)

    # 페이지가 로드될 시간을 대기
    try:
        for i in range(1, 101):  # Xpath에서는 1부터 100까지 반복
            try:
                # 아티스트 이름 Xpath
                artist_xpath = f'//ytmc-entry-row[{i}]/div/div/div[2]/div/div[1]/div/span'
                artist_name_element = wait.until(EC.presence_of_element_located((By.XPATH, artist_xpath)))
                artist_name = artist_name_element.get_attribute('textContent').strip()

                # 주간 조회수 Xpath - 두 번째 조회수를 선택
                views_xpath = f'(//div[@class="metric content center tablet-non-displayed-metric style-scope ytmc-entry-row"])[{i*2}]'
                weekly_views_element = wait.until(EC.presence_of_element_located((By.XPATH, views_xpath)))
                weekly_views_str = weekly_views_element.get_attribute('textContent').strip()

                # 조회수를 쉼표 제거 후 숫자로 변환
                weekly_views = int(weekly_views_str.replace(',', ''))

                # week_start_date를 datetime 형식으로 변환하여 timedelta 사용
                week_start_datetime = datetime.strptime(week_start_date, '%Y%m%d')
                mid_week_date = week_start_datetime - timedelta(days=4)  # 주간 중간 날짜 계산

                # 데이터 리스트에 추가 (week 항목 포함)
                artists_data.append([mid_week_date.strftime('%Y-%m-%d'), i, artist_name, weekly_views])

            except Exception as e:
                print(f"{i}위에서 에러 발생: {e}")
                continue

    except Exception as e:
        print(f"Error fetching data for week {week_start_date}: {e}")
        continue

    # 날짜를 7일 전으로 이동 (1주 전으로 설정)
    current_date -= timedelta(days=7)

# 크롬 드라이버 종료
driver.quit()

# DataFrame으로 변환 (week 항목 추가)
df = pd.DataFrame(artists_data, columns=['Week', 'Rank', 'Artist', 'Weekly Views'])

# CSV 파일로 저장
df.to_csv('youtube_artist_weekly_chart_52weeks.csv', index=False)

# 데이터 출력
print(df)
