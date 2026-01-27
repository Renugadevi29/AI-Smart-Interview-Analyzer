from flask import Blueprint, request, jsonify
from services.speech_analysis import analyze_answer
from utils.scoring import calculate_score
from services.recommendation_service import generate_personalized_learning_plan

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/analyze-interview", methods=["POST"])
def analyze_interview():
    data = request.json

    answers = data["answers"]
    domain = data["domain"]
    experience = data.get("experience", "Fresher")

    analysis = [analyze_answer(a) for a in answers]
    score_data = calculate_score(analysis)

    weaknesses = [
        "Answer clarity" if a["length_score"] < 5 else None
        for a in analysis
    ]
    weaknesses = list(filter(None, weaknesses))

    learning_plan = generate_personalized_learning_plan(
        domain,
        score_data["overall_score"],
        weaknesses,
        experience
    )

    return jsonify({
        "score": score_data,
        "analysis": analysis,
        "learning_plan": learning_plan
    })
