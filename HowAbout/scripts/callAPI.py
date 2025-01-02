import json
from googleapiclient.discovery import build

# YouTube API 설정
API_KEY = "AIzaSyDKlMcyK3peJ-woNyOLuMt5MCW_uZpOL0g"  # 자신의 API 키를 입력하세요
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


# API 호출 함수
def fetch_trending_videos(region_code="KR", max_results=50):
    """
    특정 지역의 인기 동영상 데이터를 가져옵니다.
    """
    request = youtube.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()
    return response  # 원본 데이터를 그대로 반환


# 데이터 저장 함수
def save_to_json(data, filename):
    """
    데이터를 JSON 파일로 저장합니다.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 데이터 불러오기 함수
def load_from_json(filename):
    """
    JSON 파일에서 데이터를 불러옵니다.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


# 실행
if __name__ == "__main__":
    # Step 1: API 호출 및 데이터 저장
    print("Fetching trending videos...")
    raw_data = fetch_trending_videos(region_code="KR", max_results=50)

    # JSON 파일로 원본 데이터 저장
    raw_data_filename = "trending_videos_raw.json"
    save_to_json(raw_data, raw_data_filename)
    print(f"Raw data saved to '{raw_data_filename}'")

    # Step 2: 저장된 데이터 불러오기 (예시)
    print("\nLoading saved data...")
    loaded_data = load_from_json(raw_data_filename)
    print(f"Loaded {len(loaded_data.get('items', []))} videos from saved file.")
