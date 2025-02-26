import json
import os
import pymongo
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MongoDB 연결 설정
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = pymongo.MongoClient(MONGO_URI)

# 사용할 데이터베이스 및 컬렉션 선택
db = client["test_database"]
collection_name = "keywords_popular_videos"

# 컬렉션 존재 여부 확인 후 생성
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
    print(f"✅ 컬렉션 '{collection_name}'이 생성되었습니다.")

collection = db[collection_name]

# JSON 파일 읽기
json_file_path = "/Users/82102/Desktop/howabout/howabout/youtube/scripts/keywords_popular_videos.json"  # 파일 경로
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 데이터를 MongoDB에 저장 (형식 맞춰 변환)
formatted_data = [
    {"keyword": key, "videos": values} for key, values in data.items()
]

# 중복 데이터 방지를 위해 기존 데이터 삭제 후 삽입
collection.delete_many({})
collection.insert_many(formatted_data)

print("✅ MongoDB 업로드 완료!")