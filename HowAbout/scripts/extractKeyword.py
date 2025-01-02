from konlpy.tag import Okt
from collections import Counter
import json
import pandas as pd

# JSON 데이터 로드
def load_from_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 키워드 추출 함수
def extract_keywords(data):
    """
    제목과 댓글에서 키워드를 추출합니다.
    """
    okt = Okt()
    all_words = []

    for item in data:
        # 제목과 댓글 텍스트 결합
        text = item["title"] + " " + " ".join(item["comments"])

        # 형태소 분석 및 명사 추출
        nouns = okt.nouns(text)

        # 한 글자 키워드 제거 및 불용어 처리
        stopwords = ["영상", "제목", "댓글", "입니다", "하고", "이런"]  # 필요한 불용어 추가 가능
        filtered_nouns = [noun for noun in nouns if len(noun) > 1 and noun not in stopwords]

        # 모든 단어 리스트에 추가
        all_words.extend(filtered_nouns)

    # 빈도수 계산
    word_counts = Counter(all_words)
    return word_counts.most_common(20)  # 상위 20개 키워드 반환

# 키워드 저장 함수
def save_keywords_to_csv(keywords, filename):
    """
    키워드를 CSV 파일로 저장합니다.
    """
    df = pd.DataFrame(keywords, columns=["Keyword", "Count"])
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Keywords saved to {filename}")

# 실행
if __name__ == "__main__":
    # Step 1: JSON 파일 로드
    data = load_from_json("video_details.json")
    print(f"Loaded {len(data)} videos.")

    # Step 2: 키워드 추출
    keywords = extract_keywords(data)

    # Step 3: 키워드 출력
    print("Top Keywords:")
    for rank, (keyword, count) in enumerate(keywords, start=1):
        print(f"{rank}. {keyword} - {count} occurrences")

    # Step 4: 키워드 저장
    save_keywords_to_csv(keywords, "extracted_keywords.csv")
