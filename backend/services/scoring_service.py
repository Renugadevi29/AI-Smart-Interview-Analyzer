from services.gemini_service import ask_gemini

def evaluate_answers(answers):
    strengths = []
    improvements = []

    total_possible = len(answers) * 10
    raw_score = 0

    for i, ans in enumerate(answers):
        length = len(ans.strip())

        if length > 80:
            raw_score += 10
            strengths.append(f"Answer {i+1} is well structured and detailed.")
        elif length > 40:
            raw_score += 7
            strengths.append(f"Answer {i+1} is decent but can be deeper.")
            improvements.append(f"Add more clarity and examples in Answer {i+1}.")
        else:
            raw_score += 3
            improvements.append(f"Answer {i+1} lacks depth and explanation.")

    # Normalize to 100
    final_score = round((raw_score / total_possible) * 100)

    return {
        "score": final_score,
        "strengths": strengths or ["Good attempt overall."],
        "improvements": improvements or ["Keep improving communication depth."],
        "weaknesses": improvements
    }
