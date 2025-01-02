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

    # 불용어 리스트 정의
    stopwords = ["영상", "제목", "댓글", "있습니다", "합니다", "하는", "그리고", "이나"]

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
    input_file = "video_details.csv"  # 원본 파일
    output_file = "video_details_cleaned.csv"  # 전처리 후 저장 파일

    # 전처리 수행 및 저장
    preprocess_csv(input_file, output_file)
