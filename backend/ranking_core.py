import json
from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime, timezone

def run_ranking(start_date, end_date):
    # ✅ JSON 외 출력 제거 (Node.js에서는 JSON만 받아야 하니까!)
    # print(f"조회 구간: {start_date} ~ {end_date}", flush=True)

    client = MongoClient("mongodb://localhost:27017/")
    collection = client["keyword"]["keyword"]

    alpha = 0.4
    skipped = 0
    scores = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(lambda: defaultdict(int))

    query = {
        "timestamp": {"$gte": start_date, "$lt": end_date}
    }
    # count = collection.count_documents(query)
    # print(f"해당 구간 문서 수: {count}", flush=True)

    for doc in collection.find(query):
        try:
            category = doc.get("category")
            view_count = doc.get("view_count", 0)
            published_str = doc.get("published_at")
            timestamp = doc.get("timestamp")
            combined_score = doc.get("combined_score", {})

            if not (category and published_str and timestamp and combined_score):
                # print(f"누락 필드 있음 → {doc.get('_id')}")
                skipped += 1
                continue

            published_at = datetime.fromisoformat(published_str)
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)

            hours = (timestamp - published_at).total_seconds() / 3600
            if hours <= 0:
                skipped += 1
                continue

            view_speed = view_count / hours

            for keyword, score in combined_score.items():
                scores[category][keyword] += view_speed * score
                counts[category][keyword] += 1

        except Exception:
            skipped += 1

    result = {}
    for category in scores:
        keyword_list = []
        for keyword in scores[category]:
            total = scores[category][keyword]
            count = counts[category][keyword]
            adjusted = total / (count ** alpha)
            keyword_list.append({"keyword": keyword, "score": round(adjusted, 2)})
        keyword_list.sort(key=lambda x: x["score"], reverse=True)
        result[category] = keyword_list[:50]

    # ✅ JSON만 출력
    return result 
