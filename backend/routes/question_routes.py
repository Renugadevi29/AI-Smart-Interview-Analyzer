from flask import Blueprint, request, jsonify
from services.gemini_service import ask_gemini
from routes.resume_routes import RESUME_STORAGE

question_bp = Blueprint("question_bp", __name__)

@question_bp.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.get_json()

    domain = data.get("domain")
    difficulty = data.get("difficulty")
    count = int(data.get("count", 3))
    language = data.get("language", "")
    resume_id = data.get("resume_id")

    # 🔥 Resume-based mode
    if resume_id and resume_id in RESUME_STORAGE:
        resume_text = RESUME_STORAGE[resume_id]

        prompt = f"""
Generate EXACTLY {count} interview questions
based strictly on this candidate resume.

Resume:
{resume_text}

Include:
- Technical questions from skills
- Project-based deep questions
- Behavioral questions from experience

Rules:
- Do NOT number
- One question per line
- No explanations
"""
    else:
        prompt = f"""
Generate EXACTLY {count} {difficulty}-level interview questions
for a {domain} interview.

Language: {language}

Rules:
- Do NOT number
- One question per line
- No explanations
"""

    try:
        questions = ask_gemini(prompt)
        questions = questions[:count]

        return jsonify({"questions": questions})

    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({"error": "Error generating AI response"}), 500