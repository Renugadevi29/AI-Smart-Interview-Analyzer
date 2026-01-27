from flask import Blueprint, request, jsonify
from services.gemini_service import ask_gemini

question_bp = Blueprint("question_bp", __name__)

@question_bp.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.json

    domain = data.get("domain")
    difficulty = data.get("difficulty")
    count = data.get("count", 5)
    language = data.get("language")

    prompt = f"""
Generate {count} {difficulty} level interview questions.
Domain: {domain}
"""

    if language:
        prompt += f"\nProgramming Language: {language}"

    prompt += """
Rules:
- No numbering
- No answers
- Each question in new line
"""

    text = ask_gemini(prompt)
    questions = [q.strip("- ").strip() for q in text.split("\n") if q.strip()]

    return jsonify({"questions": questions})
