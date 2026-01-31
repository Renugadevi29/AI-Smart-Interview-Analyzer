def evaluate_interview(answers):
    score = max(50, min(95, 50 + len(" ".join(answers)) // 20))

    strengths = [
        "Clear communication",
        "Relevant answers",
        "Good confidence"
    ]

    improvements = [
        "Provide more technical depth",
        "Use real-world examples"
    ]

    weaknesses = ["Technical depth"]

    return {
        "score": score,
        "strengths": strengths,
        "improvements": improvements,
        "weaknesses": weaknesses
    }
