import re


def evaluate_answers(answers):
    """
    Accepts list of STRING answers
    Returns score + feedback
    """

    total_score = 0
    strengths = []
    improvements = []
    weaknesses = []

    for i, answer in enumerate(answers):

        if not isinstance(answer, str):
            continue

        length = len(answer.split())

        # =========================
        # BASIC SCORING
        # =========================

        # Length score (0–10)
        if length < 5:
            length_score = 2
        elif length < 15:
            length_score = 5
        elif length < 30:
            length_score = 8
        else:
            length_score = 10


        # Vocabulary score
        unique_words = len(set(answer.lower().split()))

        if unique_words < 5:
            vocab_score = 3
        elif unique_words < 15:
            vocab_score = 6
        else:
            vocab_score = 9


        # Structure score (basic grammar check)
        has_full_stop = "." in answer
        has_capital = answer[0].isupper()

        structure_score = 8 if has_full_stop and has_capital else 5


        # Final score
        final = round(
            (length_score + vocab_score + structure_score) / 3,
            2
        )

        total_score += final


        # =========================
        # FEEDBACK
        # =========================

        if final >= 8:
            strengths.append(f"Answer {i+1} is clear and well explained")

        if length < 10:
            improvements.append(f"Answer {i+1} is too short")

        if not has_full_stop:
            weaknesses.append(f"Answer {i+1} lacks proper sentence ending")


    # =========================
    # FINAL RESULT
    # =========================

    if len(answers) == 0:
        avg = 0
    else:
        avg = round(total_score / len(answers), 2)

    return {
        "overall_score": avg,
        "strengths": strengths or ["Good communication skills"],
        "improvements": improvements or ["Keep practicing detailed answers"],
        "weaknesses": list(set(weaknesses))
    }
