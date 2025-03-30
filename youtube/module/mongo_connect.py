from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from collections import defaultdict

def get_data_by_date_and_category(date_str, category_id, db_name, collection_name):
    """
    주어진 날짜(KST)와 카테고리 ID로 MongoDB에서 데이터를 조회하고,
    카테고리별로 분류된 딕셔너리로 반환합니다.
    """
    # MongoDB 연결
    client = MongoClient("mongodb://localhost:27017")
    db = client[db_name]
    collection = db[collection_name]

    # KST → UTC 변환
    KST = timezone(timedelta(hours=9))
    start_kst = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=KST)
    end_kst = start_kst + timedelta(days=1)
    start_utc = start_kst.astimezone(timezone.utc)
    end_utc = end_kst.astimezone(timezone.utc)

    # 쿼리 작성
    query = {
        "timestamp": {
            "$gte": start_utc,
            "$lt": end_utc
        },
        "metadata.category_id": category_id
    }

    # 데이터 조회
    raw_data = list(collection.find(query))

    # 카테고리별로 묶기
    grouped = defaultdict(list)
    for doc in raw_data:
        cat_id = doc.get("metadata", {}).get("category_id")
        if cat_id:
            grouped[cat_id].append(doc)

    return grouped
