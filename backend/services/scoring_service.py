def evaluate_answers(answers):
    score = 0
    strengths = []
    improvements = []

    for i, ans in enumerate(answers):
        if len(ans.strip()) > 30:
            score += 10
            strengths.append(f"Answer {i+1} is clear and detailed")
        else:
            improvements.append(f"Answer {i+1} needs more explanation")

    final_score = min(score, 100)

    return {
        "score": final_score,
        "strengths": strengths or ["Attempted all questions"],
        "improvements": improvements or ["Good overall performance"]
    }
