from mapes.scoring import calculate_final_score, grade_for_score


def test_calculate_final_score_all_five():
    scores = {
        "persona_consistency": 5,
        "personality_expressiveness": 5,
        "context_awareness": 5,
        "emotional_alignment": 5,
        "multi_agent_collaboration": 5,
        "hallucination_safety": 5,
    }
    assert calculate_final_score(scores) == 100.0


def test_grade_boundaries():
    assert grade_for_score(95) == "S"
    assert grade_for_score(85) == "A"
    assert grade_for_score(75) == "B"
    assert grade_for_score(65) == "C"
    assert grade_for_score(59) == "D"
