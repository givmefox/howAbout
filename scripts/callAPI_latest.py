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
BASE_URL = "https://www.googleapis.com/youtube/v3"


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


def is_title_in_korean(title):
    """ 제목에 한글이 포함되어 있는지 확인 (한글이 없으면 영어 제목으로 간주) """
    return bool(re.search("[가-힣ㄱ-ㅎ]", title))



def get_latest_videos(category_id):
    """ 특정 카테고리의 최신 동영상 50개 가져오기 (필터링 후에도 50개 확보) """
    url = f"{BASE_URL}/search"
    params = {
        "part": "snippet",
        "type": "video",
        "videoCategoryId": category_id,
        "order": "date",
        "maxResults": MAX_RESULTS,
        "regionCode": "KR",
        "relevanceLanguage": "ko",
        "key": YOUTUBE_API_KEY
    }
    
    videos = []
    while len(videos) < 50:
        response = requests.get(url, params=params)
        data = response.json()
        if "items" in data:
            for item in data["items"]:
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                published_at = item["snippet"]["publishedAt"]

                if not is_title_in_korean(title):
                    continue
                duration_seconds = get_video_duration(video_id)
                if duration_seconds is None or duration_seconds <= 100: #100초 미만 영상 제외
                    continue

                videos.append({
                    "video_id": video_id,
                    "title": title,
                    "published_at": published_at,
                    "duration": duration_seconds
                })

                if len(videos) >= 50:
                    break

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

    return videos

    """ 특정 카테고리의 최신 동영상 50개 가져오기 (Shorts 제외, 영어 제목만 있는 영상 제외) """
    url = f"{BASE_URL}/search"
    params = {
        "part": "snippet",
        "type": "video",
        "videoCategoryId": category_id,
        "order": "date",
        "maxResults": MAX_RESULTS,
        "regionCode": "KR",
        "relevanceLanguage": "ko",
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    videos = []
    if "items" in data:
        for item in data["items"]:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            published_at = item["snippet"]["publishedAt"]

            if not is_title_in_korean(title):
                print(f"❌ {title} (영어 제목만 포함) 제외")
                continue

            duration_seconds = get_video_duration(video_id)

            if duration_seconds is None:
                print(f"⚠️ {title} (동영상 길이 정보 없음, 포함됨)")
            elif duration_seconds <= 100:
                print(f"❌ {title} (쇼츠) 제외")
                continue

            videos.append({
                "video_id": video_id,
                "title": title,
                "published_at": published_at,
                "duration": duration_seconds
            })
    
    return videos


def save_latest_videos():
    """모든 카테고리의 최신 동영상 정보 저장 (파일명: latest_videos_YYYY-MM-DD_HH-MM.json)"""
    all_videos = {}
    for category in CATEGORIES:
        print(f"▶ 카테고리 {category} 최신 동영상 수집 중...")
        all_videos[category] = get_latest_videos(category)

    # 실행 날짜 + 시간 포함한 파일명
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"latest_videos_{now}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=4)

    print(f"✅ 최신 동영상 데이터 저장 완료! ({filename})")


if __name__ == "__main__":
    save_latest_videos()
