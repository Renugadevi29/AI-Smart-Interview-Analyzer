import re

KEYWORDS = {
    "array": ["push", "append", "add"],
    "sql": ["select", "where", "join"],
    "api": ["get", "post", "json", "http"],
}


def analyze_answer(answer: str, question=""):

    words = answer.lower().split()
    word_count = len(words)

    length_score = min(word_count / 50, 1) * 10

    sentences = re.split(r"[.!?]", answer)
    structure_score = min(len(sentences) / 3, 1) * 10

    vocab_score = min(len(set(words)) / max(word_count, 1), 1) * 10

    # Detect missing keywords
    missing = []

    for key, vals in KEYWORDS.items():
        if key in question.lower():
            if not any(v in words for v in vals):
                missing.append(key)

    return {
        "length_score": round(length_score, 2),
        "structure_score": round(structure_score, 2),
        "vocab_score": round(vocab_score, 2),
        "missing_concepts": missing,
    }
