from soynlp.word import WordExtractor
import pandas as pd
import json
import os


def load_previous_results(file_path):
    """
    이전 학습 결과를 JSON 파일에서 로드합니다.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results_to_json(results, file_path):
    """
    학습 결과를 JSON 파일로 저장합니다.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def merge_results(previous_results, new_results):
    """
    이전 학습 결과와 새로운 학습 결과를 병합합니다.
    """
    for word, scores in new_results.items():
        if word in previous_results:
            # 이전 결과와 새 결과의 평균값 계산
            previous_results[word]["cohesion_forward"] = (
                previous_results[word]["cohesion_forward"] + scores["cohesion_forward"]
            ) / 2
            previous_results[word]["right_branching_entropy"] = (
                previous_results[word]["right_branching_entropy"] + scores["right_branching_entropy"]
            ) / 2
        else:
            # 새로운 단어는 추가
            previous_results[word] = scores
    return previous_results


def train_soynlp_with_json(json_path, result_file_path):
    try:
        # 1. JSON 파일 로드
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # 2. 댓글 데이터 추출
        comments = []
        for video_id, video_data in json_data.items():
            comments.extend(video_data.get("comments", []))  # 댓글 추가

        # 3. 결측치 제거 및 데이터 클리닝
        sentences = [comment.strip() for comment in comments if comment.strip()]  # 빈 댓글 제거

        # 4. Soynlp 학습
        word_extractor = WordExtractor()
        word_extractor.train(sentences)  # 학습 수행
        word_scores = word_extractor.extract()

        # 5. 학습 결과를 딕셔너리로 변환
        new_results = {
            word: {
                "cohesion_forward": score.cohesion_forward,
                "right_branching_entropy": score.right_branching_entropy,
            }
            for word, score in word_scores.items()
        }

        # 6. 이전 결과 로드 및 병합
        previous_results = load_previous_results(result_file_path)
        merged_results = merge_results(previous_results, new_results)

        # 7. 결과 저장
        save_results_to_json(merged_results, result_file_path)
        print(f"Updated results saved to {result_file_path}")

    except Exception as e:
        print(f"Error processing the file: {e}")


# 실행 부분
if __name__ == "__main__":
    # JSON 파일 경로
    data_file_path = "/Users/melon/soynlp_training_data/latest_comments_2025-02-06.json"  # 전처리된 CSV 파일 경로
    result_json_path = "/Users/melon/soynlp_training_data/word_scores.json"  # 저장할 JSON 파일 경로

    # 학습 및 결과 저장
    train_soynlp_with_json(data_file_path, result_json_path)
