import requests
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수에서 API 키 불러오기
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 카테고리 ID 리스트 (예: 1 = 영화, 10 = 음악, 15 = Pets & Animals, 17 = Sports)
CATEGORIES = [1, 10, 15, 17]
MAX_RESULTS = 50  # 한 카테고리당 최대 50개

# API URL
BASE_URL = "https://www.googleapis.com/youtube/v3"

def is_title_in_korean(title):
    """ 제목에 한글이 포함되어 있는지 확인 (한글이 없으면 영어 제목으로 간주) """
    return bool(re.search("[가-힣ㄱ-ㅎ]", title))

def parse_duration(duration):
    """ISO 8601 형식의 'PT1H26M15S' → 초 단위 변환"""
    if not duration:
        return None  

    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    matches = pattern.match(duration)

    if not matches:
        return None  

    hours = int(matches.group(1)) if matches.group(1) else 0
    minutes = int(matches.group(2)) if matches.group(2) else 0
    seconds = int(matches.group(3)) if matches.group(3) else 0

    return hours * 3600 + minutes * 60 + seconds

def get_video_duration(video_id):
    """ 특정 동영상의 길이를 가져와서 Shorts인지 판별 """
    url = f"{BASE_URL}/videos"
    params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        duration = data["items"][0]["contentDetails"].get("duration", None)
        return parse_duration(duration)  
    return None  

def get_popular_videos(category_id):
    """ 특정 카테고리의 인기 동영상 최소 50개 가져오기 (필터링 후에도 50개 확보) """
    url = f"{BASE_URL}/videos"
    params = {
        "part": "id,snippet",
        "chart": "mostPopular",
        "regionCode": "KR",
        "videoCategoryId": category_id,
        "maxResults": MAX_RESULTS,
        "key": YOUTUBE_API_KEY
    }
    
    videos = []
    next_page_token = None
    while len(videos) < 50:
        if next_page_token:
            params["pageToken"] = next_page_token
        response = requests.get(url, params=params)
        data = response.json()
        if "items" in data:
            for item in data["items"]:
                video_id = item["id"]
                title = item["snippet"]["title"]

                if not is_title_in_korean(title):
                    continue
                duration_seconds = get_video_duration(video_id)
                if duration_seconds is None or duration_seconds <= 100: #100초 미만의 영상 제외
                    continue

                videos.append({
                    "video_id": video_id,
                    "title": title
                })

                if len(videos) >= 50:
                    break

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def save_videos():
    """모든 카테고리의 인기 동영상 정보 저장"""
    all_videos = {}
    for category in CATEGORIES:
        print(f"▶ 카테고리 {category} 인기 동영상 수집 중...")
        all_videos[category] = get_popular_videos(category)

    # 실행 날짜 포함한 파일명
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"ㄷㄷㄷㄷㄷㄷㄷㄷㄷvideos_{today}.json"

    # JSON 파일로 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=4)

    print(f"✅ 인기 동영상 데이터 저장 완료! ({filename})")

if __name__ == "__main__":
    save_videos()
