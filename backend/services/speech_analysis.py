def analyze_answer(answer: str):
    length_score = min(len(answer.split()) / 50, 1.0)

    clarity = "Good" if length_score > 0.6 else "Needs improvement"

    return {
        "length_score": round(length_score * 10, 2),
        "clarity": clarity
    }
