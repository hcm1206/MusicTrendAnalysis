import json
import os
import sys
import urllib.request
import pandas as pd

# 여기에 제공된 값을 입력
client_id = "fISCIu5RYi7Z9mYYHixn"
client_secret = "YEaFHtopct"

url = "https://openapi.naver.com/v1/datalab/search"

def create_api_request_body(date, artist, new_artist):
    # Create the request body structure
    body = {
        "startDate": date,
        "endDate": date,  # Assuming same date for both start and end for daily data
        "timeUnit": "date",  # Daily data
        "keywordGroups": [
            {"groupName": artist, "keywords": [new_artist]}
        ],
        "device": "pc",
        "ages": ["1", "2", "3", "4", "5"],
        "gender": "f"
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
            return response_body.decode('utf-8')  # 응답 본문을 반환
        else:
            return f"Error Code: {rescode}"
    except urllib.error.HTTPError as e:
        return f"HTTPError: {e.code}, Message: {e.read().decode('utf-8')}"


csv_file_path = 'Transformed_Data_with_New_Artist.csv'  # CSV 파일 경로

# 데이터 로딩이 실패할 경우를 대비한 예외 처리
try:
    df_artists = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"File not found: {csv_file_path}")
    sys.exit(1)

# Loop through the dataframe and make requests for each row
results = []
for index, row in df_artists.iterrows():
    date = row['date']
    artist = row['Artist']
    new_artist = row['New_Artist']
    
    # Create the body for the API request
    body = create_api_request_body(date, artist, new_artist)
    
    # Make the API request
    response = make_api_request(body)
    
    # Store the result
    results.append({
        "date": date,
        "artist": artist,
        "new_artist": new_artist,
        "response": response
    })

# Save the results to a JSON file
output_file_path = 'D:/Last_Project/api_results.json'  # 윈도우용 경로로 수정
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# Print output file path
print("JSON 파일로 저장되었습니다:", output_file_path)

# 추가: JSON 데이터를 pandas DataFrame으로 변환 후 CSV로 저장
df_results = pd.json_normalize(results)

# 결과를 CSV 파일로 저장
csv_output_path = 'D:/Last_Project/api_results.csv'  # CSV 파일 경로
df_results.to_csv(csv_output_path, index=False, encoding='utf-8-sig')

# Print output file path
print("CSV 파일로 저장되었습니다:", csv_output_path)
