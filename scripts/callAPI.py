import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 환경 변수에서 API 키 불러오기
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 카테고리 ID 리스트 (예: 1 = 영화, 10 = 음악, 15 = Pets & Animals, 17 = Sports)
CATEGORIES = [1, 10, 15, 17]
MAX_RESULTS = 200  # 더 많은 데이터를 요청하여 필터링 후에도 충분한 개수 확보
TARGET_VIDEO_COUNT = 150  # 필터링 후 확보해야 하는 최소 영상 개수
BASE_URL = "https://www.googleapis.com/youtube/v3"


def is_title_in_korean(title):
    """ 제목에 한글이 포함되어 있는지 확인 (음악 카테고리는 예외) """
    return any("가" <= char <= "힣" or "ㄱ" <= char <= "ㅎ" for char in title)


def get_popular_videos(category_id):
    """ 특정 카테고리의 인기 동영상 150개 확보 (필터링 후 부족하면 추가 요청) """
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
    while len(videos) < TARGET_VIDEO_COUNT:
        response = requests.get(url, params=params)
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                video_id = item["id"]
                title = item["snippet"]["title"]

                # 음악(10번) 카테고리는 한글 제목 필터링 제외
                if category_id != 10 and not is_title_in_korean(title):
                    continue  # 영어 제목만 있는 영상 제외

                videos.append({
                    "video_id": video_id,
                    "title": title
                })

                if len(videos) == TARGET_VIDEO_COUNT:
                    break

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break  # 더 이상 가져올 데이터가 없으면 종료

    return videos


def save_videos():
    """모든 카테고리의 인기 동영상 정보 저장 (음악 카테고리 예외처리)"""
    all_videos = {}
    for category in CATEGORIES:
        print(f"▶ 카테고리 {category} 인기 동영상 수집 중...")
        all_videos[category] = get_popular_videos(category)

    # 실행 날짜 포함한 파일명
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"ㅁㅁㅁㅁㅁㅁvideos_{today}.json"

    # JSON 파일로 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_videos, f, ensure_ascii=False, indent=4)

    print(f"✅ 인기 동영상 데이터 저장 완료! ({filename})")


if __name__ == "__main__":
    save_videos()
