import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import glob

# 환경 변수에서 API 키 불러오기
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

BASE_URL = "https://www.googleapis.com/youtube/v3"
COMMENTS_PER_REQUEST = 100  
MAX_COMMENTS_PER_VIDEO = 4800  


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
    while len(comments) < max_comments and quota_used < 48:
        response = requests.get(url, params=params)
        data = response.json()

        if "items" in data:
            for item in data["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(comment)

        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break

        quota_used += 1  
        
    return comments


def load_latest_videos():
    """ 오늘 날짜의 모든 'latest_videos_YYYY-MM-DD_HH-MM.json' 파일을 불러와서 합침 """
    today = datetime.today().strftime("%Y-%m-%d")
    files = glob.glob(f"latest_videos_{today}_*.json")

    all_videos = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for category_videos in data.values():
                all_videos.extend(category_videos)
    
    return all_videos


def save_comments():
    """ 불러온 동영상 목록에서 제목과 댓글 데이터를 저장 """
    videos = load_latest_videos()
    comments_data = {}

    for video in videos:
        video_id = video["video_id"]
        title = video["title"]

        print(f"▶ {title} 댓글 수집 중...")
        comments = get_video_comments(video_id)
        comments_data[video_id] = {
            "title": title,
            "comments": comments
        }

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"latest_comments_{today}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(comments_data, f, ensure_ascii=False, indent=4)

    print(f"✅ 댓글 데이터 저장 완료! ({filename})")


if __name__ == "__main__":
    save_comments()
