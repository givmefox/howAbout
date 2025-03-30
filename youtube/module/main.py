from init import *
from store_video import store_trending_videos_with_comments
from kiwi import make_kiwi
from datetime import datetime, timedelta, timezone
from mongo_connect import *
from tokenize_video import tokenize_video
from analyze import *
CATEGORIES = {
    "News & Politics": "25",
    'Music' : "10",
    'Sports' : "17",
    'Gaming' : "20",
    'Science & Technology': "28"
}

def main():
    
    # 1. 동영상 데이터 가져오고 저장하기기
    store_trending_videos_with_comments()
    # 2. 데이터 가져오기
    data = get_data_by_date_and_category("2023-10-01", "trending_videos", "video_data", "trending_videos")
    # 3. kiwi 학습하기
    kiwi_objects = make_kiwi(data)
    # 4.tokenize하기
    proceesd_data = tokenize_video(data, kiwi_objects)
    
    # 5. 키워드 점수 매기기
    scored_data = score_video_keywords(proceesd_data)
    # 6. 키워드 점수 합치기
    combine_video_keyword_scores(scored_data)
    
    
    # 5. 데이터 조회
    
    kiwi_objects = make_kiwi(data)

    
    
if __name__ == "__main__":
    main()