import json
import pandas as pd
from googleapiclient.discovery import build

# YouTube API 설정
API_KEY = "AIzaSyDKlMcyK3peJ-woNyOLuMt5MCW_uZpOL0g"  # 자신의 API 키를 입력하세요
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


# JSON 파일에서 동영상 ID 로드
def load_video_ids(filename):
    """
    JSON 파일에서 동영상 ID를 추출합니다.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    video_ids = [item["id"] for item in data.get("items", [])]
    return video_ids


# 동영상 제목 및 댓글 가져오기
def fetch_video_details(video_id):
    """
    동영상 ID를 사용하여 제목 및 댓글을 가져옵니다.
    """
    # 동영상 제목 가져오기
    video_request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    video_response = video_request.execute()
    title = video_response["items"][0]["snippet"]["title"]

    # 댓글 가져오기
    comments = []
    try:
        comments_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10  # 가져올 댓글 수 조정 가능
        )
        comments_response = comments_request.execute()
        for item in comments_response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception as e:
        print(f"댓글 가져오기 실패 (ID: {video_id}): {e}")

    return {"video_id": video_id, "title": title, "comments": comments}


# 데이터 저장 함수
def save_to_json(data, filename):
    """
    데이터를 JSON 파일로 저장합니다.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_csv(data, filename):
    """
    데이터를 CSV 파일로 저장합니다.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")


# 실행
if __name__ == "__main__":
    # Step 1: JSON 파일에서 동영상 ID 로드
    video_ids = load_video_ids("trending_videos_raw.json")
    print(f"Loaded {len(video_ids)} video IDs.")

    # Step 2: 각 동영상의 제목, 댓글 및 ID 가져오기
    results = []
    for video_id in video_ids:
        details = fetch_video_details(video_id)
        results.append(details)
        print(f"Fetched details for video ID: {video_id}")

    # Step 3: 데이터 저장
    save_to_json(results, "video_details.json")
    save_to_csv(results, "video_details.csv")
    print("Data saved to 'video_details.json' and 'video_details.csv'.")
