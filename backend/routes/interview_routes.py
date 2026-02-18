from flask import Blueprint, request, jsonify
from services.gemini_service import evaluate_with_gemini
from services.recommendation_service import generate_learning_plan

interview_bp = Blueprint("interview_bp", __name__)

@interview_bp.route("/interview/submit", methods=["POST"])
def submit_interview():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        candidate = data.get("candidate")
        config = data.get("config")
        answers = data.get("answers")
        questions = data.get("questions")

        if not config:
            return jsonify({"error": "Config missing"}), 400

        if not answers or not questions:
            return jsonify({"error": "Answers or questions missing"}), 400

        # 🔥 Gemini Evaluation
        evaluation = evaluate_with_gemini(
            questions=questions,
            answers=answers,
            domain=config.get("domain")
        )

        # 🔥 Learning Plan
        learning_plan = generate_learning_plan(
            domain=config.get("domain"),
            score=evaluation.get("total_score", 0),
            weaknesses=evaluation.get("weaknesses", [])
        )

        return jsonify({
            "candidate": candidate,
            "domain": config.get("domain"),
            "difficulty": config.get("difficulty"),
            "score": evaluation.get("total_score", 0),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
            "learning_plan": learning_plan
        }), 200

    except Exception as e:
        print("❌ Interview Submission Error:", e)
        return jsonify({"error": "Interview evaluation failed"}), 500