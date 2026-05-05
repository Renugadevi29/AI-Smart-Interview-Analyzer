from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 🔹 1. Cosine similarity (Answer vs Question)
def cosine_score(answer, question):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, question])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return score * 100


# 🔹 2. Rule-based scoring
def rule_score(answer, question):
    score = 0

    answer = answer.lower()
    question_words = question.lower().split()

    # keyword matching
    for word in question_words:
        if word in answer:
            score += 5

    # length check
    if len(answer.split()) > 6:
        score += 20

    return min(score, 100)


# 🔹 3. Final hybrid score
def hybrid_score(answer, question):
    cos = cosine_score(answer, question)
    rule = rule_score(answer, question)

    return (0.7 * cos) + (0.3 * rule)