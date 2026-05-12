from datetime import date


def _urgency_score(deadline: date) -> float:
    days_left = (deadline - date.today()).days
    if days_left <= 0:
        return 10
    if days_left == 1:
        return 9
    if 2 <= days_left <= 3:
        return 8
    if 4 <= days_left <= 7:
        return 6
    if 8 <= days_left <= 14:
        return 4
    return 2


def _estimated_hours_score(estimated_hours: float) -> float:
    if estimated_hours >= 10:
        return 10
    if estimated_hours >= 6:
        return 8
    if estimated_hours >= 3:
        return 6
    if estimated_hours >= 1:
        return 4
    return 2


def calculate_task_priority(deadline: date, difficulty: int, is_exam_related: bool, estimated_hours: float) -> float:
    urgency_score = _urgency_score(deadline)
    difficulty_score = difficulty * 2
    exam_related_score = 10 if is_exam_related else 3
    estimated_score = _estimated_hours_score(estimated_hours)

    score = (
        urgency_score * 0.40
        + difficulty_score * 0.25
        + exam_related_score * 0.20
        + estimated_score * 0.15
    )
    return round(score, 2)


def get_priority_label(score: float) -> str:
    if score >= 8.5:
        return "Critical"
    if score >= 7:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def calculate_exam_revision_priority(exam_date: date, importance: int, estimated_revision_hours: float) -> float:
    urgency_score = _urgency_score(exam_date)
    importance_score = importance * 2
    hours_score = _estimated_hours_score(estimated_revision_hours)

    score = urgency_score * 0.5 + importance_score * 0.35 + hours_score * 0.15
    return round(min(score, 10), 2)
