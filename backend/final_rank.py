import json
import pymongo

# JSON 파일 로드
file_path = "/Users/82102/Desktop/howabout/howabout/youtube/scripts/final_keywords_ranking.json"

with open(file_path, "r", encoding="utf-8") as file:
    keywords_data = json.load(file)

# 순위 매기기 (점수 제외)
ranked_keywords = [{"순위": i + 1, "키워드": item[0]} for i, item in enumerate(keywords_data)]

# MongoDB 연결
mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
db = client["test_database"]
collection = db["keyword_rank"]

# 기존 데이터 삭제
collection.delete_many({})

# 데이터 삽입
collection.insert_many(ranked_keywords)

print("✅ 데이터 삽입 완료!")
