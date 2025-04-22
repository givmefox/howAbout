# ranking.py

import json
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from collections import defaultdict
import sys

def run(start_date_str, end_date_str):
    # ⏳ 날짜 파싱
    start_date = datetime.fromisoformat(start_date_str).replace(tzinfo=timezone.utc)
    end_date = datetime.fromisoformat(end_date_str).replace(tzinfo=timezone.utc)

    # MongoDB 연결
    client = MongoClient("mongodb://localhost:27017/")
    collection = client["keyword"]["keyword"]

    alpha = 0.5
    skipped = 0
    scores = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(lambda: defaultdict(int))

    query = {
        "timestamp": {"$gte": start_date, "$lt": end_date}
    }

    for doc in collection.find(query):
        try:
            category = doc.get("category")
            view_count = doc.get("view_count", 0)
            published_str = doc.get("published_at")
            timestamp = doc.get("timestamp")
            combined_score = doc.get("combined_score", {})

            if not (category and published_str and timestamp and combined_score):
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

    # 결과 계산
    result = {}
    for category in scores:
        keyword_list = []
        for keyword in scores[category]:
            total = scores[category][keyword]
            count = counts[category][keyword]
            adjusted = total / (count ** alpha)
            keyword_list.append({"keyword": keyword, "score": round(adjusted, 2)})
        keyword_list.sort(key=lambda x: x["score"], reverse=True)
        result[category] = keyword_list[:100]

    print(json.dumps(result, ensure_ascii=False))  # stdout으로 출력

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])  # start_date, end_date
