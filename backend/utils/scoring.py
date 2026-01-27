def calculate_score(answers_analysis):
    total = sum(a["length_score"] for a in answers_analysis)
    avg = total / len(answers_analysis)

    return {
        "overall_score": round(avg * 10, 2),
        "level": (
            "Excellent" if avg > 7 else
            "Good" if avg > 5 else
            "Needs Improvement"
        )
    }
