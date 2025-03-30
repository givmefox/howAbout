from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict

client = MongoClient("mongodb://localhost:27017")
db = client["howabout"]  # MongoDB 데이터베이스 이름

def get_data_by_date_and_category(from_date_str, collection_name, ):
    """
    지정한 날짜부터 오늘까지의 데이터를 MongoDB에서 가져옴.

    Args:
        from_date_str (str): 시작 날짜 (예: '2023-10-01')
        db_name (str): MongoDB 데이터베이스 이름
        collection_name (str): 컬렉션 이름
        data_type (str): 데이터 타입(예: 'trending_videos', 'comments' 등)

    Returns:
        list: 해당 범위에 해당하는 문서 리스트
    """
    # MongoDB 연결
    collection = db[collection_name]

    today_str = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d')

    query = {
        "timestamp": {
            "$gte": from_date_str,
            "$lte": today_str
        }
    }

    result = list(collection.find(query))

    # 카테고리별로 묶기
    grouped = defaultdict(list)
    for doc in result:
        cat_id = doc.get("metadata", {}).get("category_id")
        if cat_id:
            grouped[cat_id].append(doc)

    return grouped

