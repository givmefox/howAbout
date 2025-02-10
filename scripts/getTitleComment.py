import requests
import json
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# 환경 변수에서 API 키 불러오기
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# API URL
BASE_URL = "https://www.googleapis.com/youtube/v3"
COMMENTS_PER_REQUEST = 100  # API 1회 요청당 최대 100개 댓글 반환
MAX_COMMENTS_PER_VIDEO = 4800  # 동영상당 최대 4800개 댓글 수집

def get_video_comments(video_id, max_comments=MAX_COMMENTS_PER_VIDEO):
    """ 특정 동영상의 댓글 최대 4800개 가져오기 """
    comments = []
    url = f"{BASE_URL}/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": COMMENTS_PER_REQUEST,
        "key": YOUTUBE_API_KEY
    }
    quota_used = 0
    while len(comments) < max_comments and quota_used < 48:  # 48회 호출 (4800개 댓글)
        response = requests.get(url, params=params)
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(comment)

        # 다음 페이지 처리
        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

        quota_used += 1  # API 1회 호출당 1쿼터 사용
        time.sleep(0.2)  # API Rate Limit 보호

    return comments


def load_videos(filename):
    """저장된 동영상 리스트 불러오기"""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_comments(videos):
    """동영상 제목과 댓글 데이터를 저장"""
    comments_data = {}

    for category, video_list in videos.items():
        print(f"▶ 카테고리 {category}의 댓글 수집 시작...")

        for video in video_list:
            video_id = video["video_id"]
            title = video["title"]

            print(f"  - {title} ({video_id}) 댓글 수집 중...")
            comments = get_video_comments(video_id)
            comments_data[video_id] = {
                "title": title,
                "comments": comments
            }

    # 실행 날짜 포함한 파일명
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"ㅁcomments_{today}.json"

    # JSON 파일로 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(comments_data, f, ensure_ascii=False, indent=4)

    print(f"✅ 댓글 데이터 저장 완료! ({filename})")


if __name__ == "__main__":
    # 실행 날짜 기반으로 최신 파일 자동 선택
    today = datetime.today().strftime("%Y-%m-%d")
    video_filename = f"videos_{today}.json"

    if not os.path.exists(video_filename):
        print(f"❌ 파일 {video_filename}이 존재하지 않습니다. 먼저 `callAPI.py`를 실행하세요.")
    else:
        videos = load_videos(video_filename)
        save_comments(videos)
