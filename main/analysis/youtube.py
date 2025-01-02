from googleapiclient.discovery import build

API_KEY = "AIzaSyDKlMcyK3peJ-woNyOLuMt5MCW_uZpOL0g"

def get_youtube_client():
    return build("youtube", "v3", developerKey=API_KEY)

def fetch_trending_videos(region_code="KR", max_results=10):
    youtube = get_youtube_client()
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()
    return response
