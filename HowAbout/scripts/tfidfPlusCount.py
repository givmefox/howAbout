from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import pandas as pd

# TF-IDF 점수 계산 함수
def compute_tfidf(data, custom_stopwords, max_features=100):
    """
    전처리된 제목과 댓글 데이터를 결합하여 TF-IDF 점수를 계산합니다.
    """
    texts = data["title_cleaned"] + " " + data["comments_cleaned"]
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        stop_words=custom_stopwords,  # 사용자 정의 불용어 추가
        ngram_range=(1, 2)  # 단어와 2-그램 포함
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    keywords = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    return dict(zip(keywords, scores))

# 빈도수 계산 함수
def compute_frequency(data, custom_stopwords):
    """
    전처리된 제목과 댓글 데이터를 결합하여 키워드 빈도수를 계산합니다.
    """
    all_words = []
    for text in data["title_cleaned"] + " " + data["comments_cleaned"]:
        words = text.split()
        # 불용어 제거
        filtered_words = [word for word in words if word not in custom_stopwords]
        all_words.extend(filtered_words)
    return Counter(all_words)

# TF-IDF와 빈도수 결합
def combine_scores(tfidf_scores, frequency_counts, alpha=0.7, beta=0.3):
    """
    TF-IDF 점수와 빈도수를 결합하여 최종 점수를 계산합니다.
    """
    combined_scores = {}
    all_keywords = set(tfidf_scores.keys()).union(set(frequency_counts.keys()))
    for keyword in all_keywords:
        tfidf_score = tfidf_scores.get(keyword, 0)
        frequency_score = frequency_counts.get(keyword, 0)
        combined_scores[keyword] = tfidf_score * alpha + frequency_score * beta
    return sorted(combined_scores.items(), key=lambda x: -x[1])

# 실행
if __name__ == "__main__":
    # 사용자 정의 불용어 리스트
    custom_stopwords = [
        "진짜", "정말", "항상", "보고", "사람", "시간", "마음", "생각", "축하",
        "응원", "방송", "준비", "새해", "처음", "한국", "노래" ,"지금" ,"마지막" , "다시", "사랑", "최고"
    ]

    # Step 1: 전처리된 CSV 파일 로드
    input_file = "video_details_cleaned.csv"
    data = pd.read_csv(input_file, encoding="utf-8")
    print(f"Loaded {len(data)} rows from '{input_file}'")

    # 결측값 확인 및 처리
    if data.isnull().sum().sum() > 0:
        print("결측값이 발견되었습니다. 처리 중...")
        data["title_cleaned"] = data["title_cleaned"].fillna("")  # 제목 결측값을 빈 문자열로 대체
        data["comments_cleaned"] = data["comments_cleaned"].fillna("")  # 댓글 결측값을 빈 문자열로 대체
        print("결측값 처리가 완료되었습니다.")

    # Step 2: TF-IDF 점수 계산
    tfidf_scores = compute_tfidf(data, custom_stopwords, max_features=100)
    print("TF-IDF 계산 완료.")

    # Step 3: 빈도수 계산
    frequency_counts = compute_frequency(data, custom_stopwords)
    print("빈도수 계산 완료.")

    # Step 4: 점수 결합
    combined_keywords = combine_scores(tfidf_scores, frequency_counts, alpha=0.7, beta=0.3)

    # Step 5: 상위 키워드 출력
    print("Top Combined Keywords:")
    for rank, (keyword, score) in enumerate(combined_keywords[:20], start=1):
        print(f"{rank}. {keyword} - {score:.4f}")

    # Step 6: 키워드 저장
    output_file = "combined_keywords.csv"
    df = pd.DataFrame(combined_keywords, columns=["Keyword", "Score"])
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Combined Keywords saved to '{output_file}'")
