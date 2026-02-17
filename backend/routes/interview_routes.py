from flask import Blueprint, request, jsonify
from services.gemini_service import evaluate_with_gemini
from services.recommendation_service import generate_learning_plan

interview_bp = Blueprint("interview_bp", __name__)

@interview_bp.route("/interview/submit", methods=["POST"])
def submit_interview():
    try:
        data = request.get_json()

        candidate = data.get("candidate")
        config = data.get("config")
        answers = data.get("answers")
        questions = data.get("questions")

        if not candidate or not answers or not questions:
            return jsonify({"error": "Invalid payload"}), 400

        # 🔥 STRICT AI EVALUATION
        evaluation = evaluate_with_gemini(
            questions=questions,
            answers=answers,
            domain=config.get("domain")
        )

        total_score = evaluation.get("total_score", 0)
        strengths = evaluation.get("strengths", [])
        weaknesses = evaluation.get("weaknesses", [])
        improvements = evaluation.get("improvements", [])

        # 🎯 DOMAIN BASED LEARNING PLAN
        learning_plan = generate_learning_plan(
            domain=config.get("domain"),
            score=total_score,
            weaknesses=weaknesses
        )

        return jsonify({
            "candidate": candidate,
            "domain": config.get("domain"),
            "difficulty": config.get("difficulty"),
            "score": total_score,
            "strengths": strengths,
            "improvements": improvements,
            "learning_plan": learning_plan
        }), 200

    except Exception as e:
        print("❌ Interview Submission Error:", e)
        return jsonify({"error": "Interview evaluation failed"}), 500
