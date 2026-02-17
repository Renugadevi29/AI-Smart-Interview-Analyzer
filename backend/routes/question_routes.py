from flask import Blueprint, request, jsonify
from services.gemini_service import ask_gemini

question_bp = Blueprint("question_bp", __name__)

@question_bp.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.get_json()

    domain = data.get("domain")
    difficulty = data.get("difficulty")
    count = int(data.get("count", 3))
    language = data.get("language", "")

    prompt = f"""
Generate EXACTLY {count} {difficulty}-level interview questions
for a {domain} interview.

Language: {language}

IMPORTANT RULES:
- Return exactly {count} questions
- Do NOT number them
- Do NOT add explanations
- Each question must be on a new line
"""

    try:
        questions = ask_gemini(prompt)

        # Safety check: trim or pad to exact count
        questions = questions[:count]

        return jsonify({"questions": questions})

    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({"error": "Error generating AI response"}), 500
