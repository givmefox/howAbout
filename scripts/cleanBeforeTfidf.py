import pandas as pd
import re
from konlpy.tag import Okt

# 텍스트 정제 함수
def clean_text(text):
    """
    텍스트 데이터에서 HTML 태그, URL, 특수문자, 숫자 등을 제거합니다.
    """
    text = re.sub(r"<[^>]+>", "", text)  # HTML 태그 제거
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # URL 제거
    text = re.sub(r"\d+", "", text)  # 숫자 제거
    text = re.sub(r"[^\w\s]", "", text)  # 특수문자 제거
    return text.strip()

# Konlpy 전처리 함수
def preprocess_with_konlpy(text, stopwords):
    """
    Konlpy를 사용하여 명사를 추출하고 불용어 및 한 글자 단어를 제거합니다.
    """
    okt = Okt()
    tokens = okt.pos(text)
    filtered_tokens = [word for word, tag in tokens if tag in ["Noun", "ProperNoun"]]
    # 불용어 제거 및 한 글자 단어 필터링
    filtered_tokens = [word for word in filtered_tokens if word not in stopwords and len(word) > 1]
    return " ".join(filtered_tokens)

# CSV 파일 전처리 함수
def preprocess_csv(input_file, output_file):
    """
    CSV 파일에서 텍스트 데이터를 전처리하고 저장합니다.
    """
    # CSV 파일 로드
    df = pd.read_csv(input_file, encoding="utf-8")

    stopwords = [
        # 조사
        "은", "는", "이", "가", "을", "를", "의", "에", "와", "과", "도", "로", "으로", "에서",
        # 접속사
        "그리고", "그래서", "하지만", "또는",
        # 빈번히 사용되는 표현
        "진짜", "정말", "그냥", "이제", "너무", "항상", "계속", "요즘", "바로",
        # 긍정 표현 및 감탄사
        "최고", "완전", "대박", "멋지다", "웃기다", "귀엽다", "아", "와", "오", "헐", "우와", "어머", "응", "음", "앗",
        # 시간 표현
        "오늘", "어제", "내일", "지금", "방금", "곧",
        # 플랫폼 관련
        "영상", "동영상", "댓글", "채널", "조회수", "좋아요", "구독", "공유", "업로드", "시청",
        # 빈번히 등장하는 무의미 단어
        "사람", "우리", "모두", "자신", "다른", "모든", "이거", "그것", "이번", "한국", "이번", "시간", "세상", "행복",
        # 데이터에서 추출된 무의미 단어
        "응원", "축하", "새해", "마음", "가족", "위해", "정말", "계속", "우리나라", "이번", "모두", "생각"
    ]

    # 제목과 댓글 전처리
    df["title_cleaned"] = df["title"].apply(lambda x: preprocess_with_konlpy(clean_text(x), stopwords))
    df["comments_cleaned"] = df["comments"].apply(
        lambda x: " ".join(
            [preprocess_with_konlpy(clean_text(comment), stopwords) for comment in eval(x)]
        )
    )

    # 전처리 결과 저장
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Preprocessed data saved to '{output_file}'")

# 실행
if __name__ == "__main__":
    # 원본 파일과 저장할 파일 이름 설정
    input_file = "comments_2025-02-05.json"  # 원본 파일
    output_file = "video_details_cleaned.json"  # 전처리 후 저장 파일

    # 전처리 수행 및 저장
    preprocess_csv(input_file, output_file)