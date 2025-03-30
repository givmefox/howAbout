from kiwipiepy import Kiwi
import os

def make_kiwi(data, user_dict_path="user_dict.txt"):
    kiwi_objects = {}

    # 기존 사용자 사전 로딩용 집합
    existing_words = set()
    if os.path.exists(user_dict_path):
        with open(user_dict_path, "r", encoding="utf-8") as f:
            for line in f:
                word, _ = line.strip().split("\t")
                existing_words.add(word)

    # 키위 만들기
    
    for category, videos in data.items():
        kiwi = Kiwi()

        if os.path.exists(user_dict_path):
            kiwi.load_user_dictionary(user_dict_path)

        category_comments = []
        for video in videos:
            comments = video.get("comments", [])
            spaced_comments = [kiwi.space(comment, reset_whitespace=True) for comment in comments]
            video_comment = " ".join(spaced_comments)
            category_comments.append(video_comment)

        print(f"📂 Category: {category}")
        scores = kiwi.extract_add_words(
            category_comments,
            min_cnt=5,
            max_word_len=10,
            min_score=0.1,
            pos_score=0.0
        )
        for word, final_score, freq, pos_score in scores:
            print(f"단어: {word}, 점수: {final_score:.3f}, 출현 빈도: {freq}, 품사 점수: {pos_score:.3f}")

        # 새로운 단어들을 user_dict.txt에 추가
        with open(user_dict_path, "a", encoding="utf-8") as f:
            for word, final_score, freq, pos_score in scores:
                if word not in existing_words:
                    f.write(f"{word}\tNNP\n")
                    existing_words.add(word)
                    print(f"📝 사전 추가됨: {word} (score={final_score:.3f}, freq={freq})")

         # 📌 새로 만든 kiwi에 최종 사전 로드
        final_kiwi = Kiwi()
        final_kiwi.load_user_dictionary(user_dict_path)

        kiwi_objects[category] = final_kiwi

    return kiwi_objects
