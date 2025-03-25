def normalize_keywords(raw_string):
    """
    사용자가 입력한 문자열에서 비슷한 단어들을 표준 키워드로 정규화
    예: "귀여움", "귀엽다" → "귀여운"
    """
    mapping = {
        "귀여움": "귀여운", "귀엽다": "귀여운", "귀여운 외모": "귀여운",
        "섹시함": "섹시한", "섹시": "섹시한", "섹시한 매력": "섹시한",
        "활발함": "활발한", "에너지 넘침": "활발한",
        "조용함": "조용한", "차분함": "조용한",
        "지적임": "지적인", "지적인 사람": "지적인"
    }
    keywords = [word.strip().lower() for word in raw_string.split(',') if word.strip()]
    normalized = [mapping.get(word, word) for word in keywords]
    return set(normalized)


def keyword_similarity(str1, str2):
    set1 = normalize_keywords(str1)
    set2 = normalize_keywords(str2)
    return len(set1 & set2)


def age_similarity(current_user, other_users, diff=4):
    current_age = int(current_user['age'])
    candidates = [
        (u, abs(current_age - int(u['age'])))
        for u in other_users if u['age'] and abs(current_age - int(u['age'])) <= diff
    ]
    return sorted(candidates, key=lambda x: x[1])[:2]


def mbti_similarity(current_user, other_users):
    def score(a, b):
        return sum(1 for x, y in zip(a, b) if x == y)

    candidates = [
        (u, score(current_user['mbti'], u['mbti']))
        for u in other_users if u['mbti']
    ]
    return sorted(candidates, key=lambda x: -x[1])[:2]


def hobbies_similarity(current_user, other_users):
    candidates = [
        (u, keyword_similarity(current_user['hobbies'], u['hobbies']))
        for u in other_users if u['hobbies']
    ]
    return sorted(candidates, key=lambda x: -x[1])[:2]


def music_similarity(current_user, other_users):
    candidates = [
        (u, keyword_similarity(current_user['music_style'], u['music_style']))
        for u in other_users if u['music_style']
    ]
    return sorted(candidates, key=lambda x: -x[1])[:2]


def ideal_match(current_user, other_users):
    matches = []
    for u in other_users:
        if u['gender'] == current_user['gender']:
            continue  # 이성만 추천

        try:
            age_diff = abs(int(current_user['age']) - int(u['age']))
            max_diff = int(current_user['ideal_age_diff'])
            if age_diff > max_diff:
                continue

            if current_user['ideal_mbti'] and current_user['ideal_mbti'] not in u['mbti']:
                continue

            if current_user['ideal_personality'] and keyword_similarity(current_user['ideal_personality'], u['personality']) == 0:
                continue

            if current_user['ideal_appearance'] and keyword_similarity(current_user['ideal_appearance'], u['appearance']) == 0:
                continue

            min_h, max_h = map(int, current_user['ideal_height_range'].split('~'))
            if not (min_h <= int(u['height']) <= max_h):
                continue

            min_w, max_w = map(int, current_user['ideal_weight_range'].split('~'))
            if not (min_w <= int(u['weight']) <= max_w):
                continue

            if current_user['ideal_body_shape'] and keyword_similarity(current_user['ideal_body_shape'], u['body_shape']) == 0:
                continue

            matches.append(u)

        except:
            continue

    return matches[:2]
