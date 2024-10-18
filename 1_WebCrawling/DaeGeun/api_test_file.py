import json
import os
import time
import urllib.request
import pandas as pd
import urllib.error
import logging  # 로그 기록을 위한 추가 모듈

# 로그 설정
logging.basicConfig(filename='api_request.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 여기에 제공된 값을 입력
# (2024-09-26)

# 대근
# client_id = "fISCIu5RYi7Z9mYYHixn"
# client_secret = "YEaFHtopct"

# 지훈 
client_id = "lCA8LFLcRR1cGgcfIesR"
client_secret = "svkDAu7FUq"

# 진우
# client_id = "nqO1q20si0Nu9yBxeNM0"
# client_secret = "JCUXxMt6mk"

# 창민 
# client_id = "sMr2_6qjZ4bp0mxZoWOp"
# client_secret = "icNwNiPkT9"

# 재형 
# client_id = "ndoVgdNtP3oaKB7AFonP"
# client_secret = "e7A2QygYPd"


url = "https://openapi.naver.com/v1/datalab/search"

def create_api_request_body(artist):
    # 요청 본문 생성 (groupName과 keywords 모두 artist로 설정)
    body = {
        "startDate": "2023-09-18",
        "endDate": "2024-09-09",
        "timeUnit": "week",
        "keywordGroups": [
            {"groupName": artist, "keywords": [artist]}
        ],
    }
    return json.dumps(body)

def make_api_request(body):
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    request.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))  # 응답 본문을 JSON으로 변환
        else:
            logging.error(f"Error Code: {rescode} for request: {body}")
            return {"error": f"Error Code: {rescode}"}
    
    except urllib.error.HTTPError as e:
        logging.error(f"HTTPError: {e.code}, Message: {e.read().decode('utf-8')} for request: {body}")
        return {"error": f"HTTPError: {e.code}, Message: {e.read().decode('utf-8')}"}
    
    except urllib.error.URLError as e:
        logging.error(f"URLError: {e.reason} for request: {body}")
        return {"error": f"URLError: {e.reason}"}
    
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON response for request: {body}")
        return {"error": "Failed to decode JSON response"}

# CSV 파일에서 전체 데이터 불러오기
csv_file_path = 'cleaned_artists.csv'
df_artists = pd.read_csv(csv_file_path)

# Loop through the dataframe and make requests for each row
results = []
for index, row in df_artists.iterrows():
    artist = row['Artist']
    
    # Create the body for the API request
    body = create_api_request_body(artist)
    
    # Make the API request
    response = make_api_request(body)
    
    # Store the result
    results.append({
        "artist": artist,
        "response": response
    })
    
    # 진행 상황 로그 기록
    logging.info(f"Processed request for artist: {artist}")

    # API 호출 빈도 제한을 위해 딜레이 추가 (1초)
    time.sleep(2)

# JSON 데이터를 pandas DataFrame으로 변환
df_results = pd.json_normalize(results)

# 결과를 CSV 파일로 저장
csv_output_path = 'api_results5.csv'
df_results.to_csv(csv_output_path, index=False, encoding='utf-8-sig')

# 완료 메시지 출력 및 로그 기록
print("CSV 파일로 저장되었습니다:", csv_output_path)
logging.info("CSV 파일로 저장되었습니다: " + csv_output_path)