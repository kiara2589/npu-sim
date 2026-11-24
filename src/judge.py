EPSILON = 1e-9

def normalize_label(raw):
    """
    다양한 유형의 라벨 입력을 표준 라벨('Cross', 'X')로 정규화.
    알 수 없는 입력은 None 반환.
    """
    if raw is None:
        return None
    key = str(raw).strip().lower()
    if key in ("+", "cross", "plus"):
        return "Cross"
    if key in ("x", "ex"):
        return "X"
    return None

def judge(score_a, score_b, label_a="Cross", label_b="X"):
    """
    허용오차(epsilon) 기반 두 필터 점수 비교 및 판정.
    |a - b| < EPSILON 인 경우 동점(UNDECIDED)으로 판정.
    """
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    return label_a if score_a > score_b else label_b